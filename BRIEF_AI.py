import os
import logging
import warnings
import re
from newspaper import Article
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = ""
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
title_generator = pipeline("text2text-generation", model="google/pegasus-xsum")
sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model)

def escape_markdown(text):
    """Escape special characters for Telegram MarkdownV2 formatting."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Hello! Send me a news article link, and I'll summarize it for you!")

def extract_news_details(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title or "Unknown Title",
            "author": ", ".join(article.authors) if article.authors else "Unknown",
            "publication_date": str(article.publish_date) if article.publish_date else "Unknown",
            "content": article.text or ""
        }
    except Exception as e:
        return {"error": f"Failed to extract article: {str(e)}"}


def summarize_text(content):
    try:
        summary = summarizer(content, max_length=120, min_length=50, num_beams=5, truncation=True)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error in summarization: {str(e)}"


def generate_title(summary):
    try:
        prompt = f"Write a two-word catchy title for this news article: {summary}"
        title = title_generator(prompt, max_length=20, min_length=7, num_beams=8, truncation=True)
        return title[0]['generated_text'].strip()
    except Exception as e:
        return f"Error in title generation: {str(e)}"


def detect_tone(content):
    try:
        result = sentiment_analyzer(content[:512])  
        sentiment_label = result[0]['label']
        return "NEGATIVE" if sentiment_label == "LABEL_0" else "NEUTRAL" if sentiment_label == "LABEL_1" else "POSITIVE"
    except Exception as e:
        return f"Error in sentiment analysis: {str(e)}"


def categorize_news(summary):
    labels = ["Politics", "Technology", "Sports", "Health", "Business", "Science", "World"]
    try:
        result = classifier(summary, candidate_labels=labels)
        return result["labels"][0]
    except Exception as e:
        return f"Error in categorization: {str(e)}"


async def process_news(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    processing_msg = await update.message.reply_text("⏳ Processing your article...")

    try:
        await processing_msg.edit_text("🔍 Extracting content from the link...")
        details = extract_news_details(url)

        if "error" in details:
            await processing_msg.edit_text(f"⚠️ Unable to process this news article:\n{details['error']}")
            return

        content = details["content"]
        if not content:
            await processing_msg.edit_text("⚠️ No content found in the article.")
            return
        await processing_msg.edit_text("📝 Summarizing the article...")
        summary = summarize_text(content)
        await processing_msg.edit_text("🖊 Generating a catchy title...")
        generated_title = generate_title(summary)
        await processing_msg.edit_text("🎭 Analyzing the article's tone...")
        tone = detect_tone(content)
        await processing_msg.edit_text("📂 Classifying the news category...")
        category = categorize_news(summary)
        await processing_msg.delete()
        response = (
            f"📰 News Summary:\n"
            f"📌 Title: {generated_title}\n"
            f"📅 Published Date: {details['publication_date']}\n"
            f"📝 Summary: {summary}\n"
            f"📂 Category: {category}\n"
            f"🎭 Tone: {tone}\n"
        )
        escaped_response = escape_markdown(response)
        if len(escaped_response) > 4000:
            for i in range(0, len(escaped_response), 4000):
                await update.message.reply_text(escaped_response[i:i+4000], parse_mode="MarkdownV2")
        else:
            await update.message.reply_text(escaped_response, parse_mode="MarkdownV2")
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_news))
    logging.info("🤖 Bot is running...")
    app.run_polling()
if __name__ == "__main__":
    main()
