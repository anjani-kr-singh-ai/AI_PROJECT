# AI News Processing Bots 🤖📰

This repository contains two powerful AI-driven Telegram bots for news processing and analysis. Both bots leverage state-of-the-art natural language processing models to provide intelligent news summarization, sentiment analysis, and categorization.

## 🎯 Overview

### BRIEF_AI Bot
A comprehensive news article analyzer that processes individual news article URLs and provides:
- **Smart Summarization**: Condenses articles into digestible summaries
- **Auto Title Generation**: Creates catchy two-word titles
- **Sentiment Analysis**: Detects article tone (Positive/Neutral/Negative)
- **Category Classification**: Automatically categorizes news into topics
- **Topic Modeling**: Advanced content analysis using BERTopic

### NEWS_AI Bot
A category-based news aggregator that fetches and processes multiple articles:
- **Category Search**: Fetches top 3 articles for any category
- **Batch Processing**: Processes multiple articles simultaneously
- **Real-time Updates**: Live status updates during processing
- **Comparative Analysis**: Shows both original and AI-generated titles

## 🚀 Features

### Common Features
- ✅ **Advanced NLP Models**: Uses Facebook BART, Google Pegasus, and RoBERTa
- ✅ **Telegram Integration**: Seamless bot interaction
- ✅ **Error Handling**: Robust error management and user feedback
- ✅ **Markdown Formatting**: Rich text formatting for better readability
- ✅ **Content Extraction**: Automatic article parsing and cleaning

### BRIEF_AI Specific
- 🔍 **URL Processing**: Direct article URL analysis
- 🏷️ **Topic Modeling**: BERTopic integration for advanced topic detection
- 📊 **Detailed Analytics**: Comprehensive article metadata extraction
- 🎨 **Advanced Formatting**: MarkdownV2 support with character escaping

### NEWS_AI Specific
- 🌐 **GNews API Integration**: Real-time news fetching
- 📱 **Category-based Search**: User-defined category exploration
- 🔄 **Batch Processing**: Multiple article analysis
- ⏱️ **Progress Tracking**: Real-time processing updates

## 🛠️ Technology Stack

### Core AI Models
- **Summarization**: `facebook/bart-large-cnn`
- **Title Generation**: `google/pegasus-xsum`
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment`
- **Classification**: `facebook/bart-large-mnli`
- **Embeddings**: `all-MiniLM-L6-v2` (SentenceTransformers)
- **Topic Modeling**: BERTopic with custom embeddings

### Libraries & Frameworks
- **Telegram Bot**: `python-telegram-bot`
- **NLP Processing**: `transformers`, `sentence-transformers`
- **Web Scraping**: `newspaper3k`
- **Topic Modeling**: `bertopic`
- **Text Processing**: `nltk`
- **API Requests**: `requests`

## 📋 Prerequisites

```bash
pip install python-telegram-bot
pip install transformers
pip install torch
pip install newspaper3k
pip install sentence-transformers
pip install bertopic
pip install nltk
pip install requests
```

## ⚙️ Configuration

### BRIEF_AI Setup
1. **Telegram Bot Token**: Replace `BOT_TOKEN = ""` with your bot token
2. **Model Downloads**: Models will auto-download on first run
3. **Dependencies**: Ensure all required packages are installed

### NEWS_AI Setup
1. **Telegram Bot Token**: Replace `TELEGRAM_BOT_TOKEN = ""` with your bot token
2. **GNews API Key**: Replace `GNEWS_API_KEY = ""` with your API key from [GNews.io](https://gnews.io/)
3. **NLTK Data**: The bot will auto-download required NLTK data

## 🚀 Usage

### Running BRIEF_AI
```python
python BRIEF_AI.py
```

**Bot Commands:**
- `/start` - Initialize the bot
- Send any news article URL to get comprehensive analysis

**Example Output:**
```
📰 News Summary:
📌 Title: Tech Innovation
📅 Published Date: 2024-01-15
📝 Summary: [AI-generated summary]
📂 Category: Technology
🎭 Tone: POSITIVE
```

### Running NEWS_AI
```python
python NEWS_AI.py
```

**Bot Commands:**
- `/start` - Initialize the bot
- Send any category name (e.g., "Technology", "Sports", "Health")

**Example Output:**
```
📰 Original Title: [Original article title]
🔖 Generated Title: [AI-generated title]
👤 Author: [Author name]
📅 Published Date: [Publication date]
📊 Tone: [Sentiment analysis]
🔎 Summary: [Article summary]
🔗 Read Full Article
```

## 🔧 API Requirements

### BRIEF_AI
- **Telegram Bot API**: Create a bot via [@BotFather](https://t.me/BotFather)

### NEWS_AI
- **Telegram Bot API**: Create a bot via [@BotFather](https://t.me/BotFather)
- **GNews API**: Register at [GNews.io](https://gnews.io/) for news fetching

## 📊 Model Performance

### Summarization Quality
- **Model**: Facebook BART-large-CNN
- **Summary Length**: 50-120 tokens (BRIEF_AI), 30-60 tokens (NEWS_AI)
- **Beam Search**: 5-8 beams for optimal quality

### Sentiment Accuracy
- **Model**: Cardiff RoBERTa-base
- **Categories**: Positive, Neutral, Negative
- **Input Limit**: 512 characters for optimal performance

### Classification Precision
- **Categories**: Politics, Technology, Sports, Health, Business, Science, World
- **Method**: Zero-shot classification
- **Confidence**: Returns top category with confidence scores

## 🛡️ Error Handling

Both bots include comprehensive error handling:
- **Network Issues**: Graceful handling of API timeouts
- **Invalid URLs**: User-friendly error messages
- **Content Extraction**: Fallback mechanisms for difficult sites
- **Rate Limiting**: Built-in delays to prevent API throttling
- **Long Text**: Automatic message splitting for Telegram limits

## 🔒 Security Features

- **Input Validation**: URL and text sanitization
- **Token Protection**: Environment variable support recommended
- **Markdown Escaping**: Prevents injection via special characters
- **Error Sanitization**: Safe error message display

## 📝 Logging

Both bots include comprehensive logging:
- **Info Level**: Bot startup and operation status
- **Error Tracking**: Detailed error logs for debugging
- **User Actions**: Anonymous usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Please ensure compliance with model licenses:
- BART: Apache 2.0
- RoBERTa: MIT
- Pegasus: Apache 2.0

## 🆘 Troubleshooting

### Common Issues
1. **Model Download Errors**: Ensure stable internet connection
2. **Memory Issues**: Consider using CPU-only mode for limited resources
3. **API Rate Limits**: Implement exponential backoff
4. **Telegram Formatting**: Check for unescaped special characters

### Performance Optimization
- **Model Caching**: Models are cached after first load
- **Batch Processing**: NEWS_AI processes articles sequentially to manage resources
- **Memory Management**: Automatic cleanup of large article content

## 📞 Support

For issues, suggestions, or contributions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using cutting-edge AI technologies**