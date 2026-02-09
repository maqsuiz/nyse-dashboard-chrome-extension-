# NYSE News Dashboard

Real-time stock market news dashboard with two versions:
- **Streamlit Web App** - Full-featured Python web application
- **Chrome Extension** - Browser extension for quick access

## Features

- Live market prices (Gold, USD, EUR, BTC, S&P 500, BIST 100)
- Financial news aggregation from multiple sources
- Sentiment analysis (Positive/Negative/Neutral)
- Hype score algorithm for news prioritization
- Time-based filtering
- Monthly market movement insight

---

## Streamlit Web App

### Installation

```bash
pip install -r requirements.txt
streamlit run main.py
```

### Requirements
- Python 3.8+
- streamlit, GoogleNews, textblob, pandas, yfinance, feedparser

---

## Chrome Extension

### Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder

---

## Project Structure

```
nyse-news-dashboard/
├── main.py              # Streamlit app
├── requirements.txt     # Python dependencies
├── README.md
├── .gitignore
└── chrome-extension/    # Browser extension
    ├── manifest.json
    ├── popup.html
    ├── popup.css
    └── popup.js
```

## License

MIT License

