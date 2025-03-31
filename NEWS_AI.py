import os
import logging
import requests
import nltk
import asyncio
from newspaper import Article
from transformers import pipeline
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes
logging.basicConfig(level=logging.INFO)
nltk.download("punkt")
TELEGRAM_BOT_TOKEN = ""
GNEWS_API_KEY = ""
GNEWS_URL = "https://gnews.io/api/v4/search"
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
title_generator = pipeline("text2text-generation", model="google/pegasus-xsum")
sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")
def fetch_news_articles(cat):
    try:
        params = {
            "q": cat,
            "lang": "en",
            "country": "us",
            "max": 3,
            "apikey": GNEWS_API_KEY
        }
        response = requests.get(GNEWS_URL, params=params)
        data = response.json()
        
        if "articles" not in data or not data["articles"]:
            return {"error": "No articles found for this category."}

        return data["articles"][:3]
    except Exception as e:
        return {"error": f"Failed to fetch news: {str(e)}"}
def extract_news_details(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "author": article.authors if article.authors else ["Unknown"],
            "publication_date": str(article.publish_date) if article.publish_date else "Unknown",
            "content": article.text
        }
    except Exception as e:
        return {"error": f"Failed to extract article: {str(e)}"}
def summarize_text(content):
    try:
        summary = summarizer(content, max_length=60, min_length=30, num_beams=5, truncation=True)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error in summarization: {str(e)}"
def generate_title(summary):
    try:
        prompt = f"Write a short, catchy title for this news: {summary}"
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
def process_news_article(url):
    details = extract_news_details(url)

    if "error" in details:
        return details

    content = details["content"]
    if not content:
        return {"error": "No content found in the article."}

    summary = summarize_text(content)
    generated_title = generate_title(summary)
    tone = detect_tone(content)

    return {
        "URL": url,
        "Original Title": details["title"],
        "Generated Title": generated_title,
        "Author": details["author"],
        "Published Date": details["publication_date"],
        "Summary": summary,
        "Tone": tone
    }
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the AI News Summarizer Bot! 📰\n"
        "Please type a category (e.g., 'Technology', 'Sports', 'Health') and I'll fetch the latest news for you."
    )
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text.strip()

    loading_message = await update.message.reply_text(f"🔎 Searching for top 3 news articles in *{category}*...\nThis may take a few seconds.", parse_mode="Markdown")

    articles = fetch_news_articles(category)

    if "error" in articles:
        await loading_message.edit_text(f"⚠️ {articles['error']}")
        return

    for index, article in enumerate(articles):
        await asyncio.sleep(1)  # Simulate loading time
        await loading_message.edit_text(f"📢 Fetching article {index + 1} of 3...")

        url = article["url"]
        result = process_news_article(url)

        if "error" in result:
            await update.message.reply_text(f"⚠️ {result['error']}")
            continue

        response = (
            f"📰 Original Title: {result['Original Title']}\n"
            f"🔖 Generated Title: {result['Generated Title']}\n"
            f"👤 Author: {', '.join(result['Author'])}\n"
            f"📅 Published Date: {result['Published Date']}\n"
            f"📊 Tone: {result['Tone']}\n"
            f"🔎 Summary:\n{result['Summary']}\n\n"
            f"🔗 [Read Full Article]({result['URL']})"
        )

        await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)

    await loading_message.delete()
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
if __name__ == "__main__":
    main()
