# NYSE News Dashboard - Chrome Extension

A Chrome browser extension that displays real-time stock market news and prices.

## Features

- Live market prices (Gold, USD, EUR, BTC, S&P 500)
- Financial news aggregation
- Sentiment analysis
- Hype score ranking
- Time-based filtering

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `nyse-extension` folder
5. Click the extension icon in toolbar

## Files

```
nyse-extension/
├── manifest.json   # Extension config
├── popup.html      # Main UI
├── popup.css       # Styles
├── popup.js        # Logic
└── icons/          # Extension icons
```

## Usage

Click the extension icon to open the popup. Use time filters (1H, 4H, 12H, 24H) and Refresh button to update data.

## Note

If icons are missing, you can use any 16x16, 48x48, and 128x128 PNG images named `icon16.png`, `icon48.png`, `icon128.png` in the icons folder.
