// NYSE News Dashboard - Chrome Extension
// Main JavaScript file

// Configuration
const HYPE_KEYWORDS = ['surge', 'crash', 'record', 'breaking', 'soar', 'plunge', 'historic',
    'skyrocket', 'collapse', 'boom', 'bust', 'shock', 'alert', 'critical', 'rally'];

const POSITIVE_WORDS = ['surge', 'rally', 'gain', 'rise', 'up', 'high', 'record', 'boom', 'soar', 'growth', 'profit', 'win'];
const NEGATIVE_WORDS = ['crash', 'fall', 'drop', 'down', 'low', 'plunge', 'collapse', 'bust', 'loss', 'fear', 'worry', 'crisis'];

// Market tickers
const TICKERS = [
    { symbol: 'GC=F', name: 'GOLD' },
    { symbol: 'DX=F', name: 'USD' },
    { symbol: 'EURUSD=X', name: 'EUR' },
    { symbol: 'BTC-USD', name: 'BTC' },
    { symbol: '^GSPC', name: 'S&P 500' }
];

// RSS Feeds with working CORS proxies
const RSS_FEEDS = [
    'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EGSPC&region=US&lang=en-US'
];

// CORS Proxies to try
const CORS_PROXIES = [
    'https://api.allorigins.win/raw?url=',
    'https://corsproxy.io/?'
];

// State
let selectedHours = 24;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadMarketData();
    loadNews();
    loadInsight();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Time filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            selectedHours = parseInt(e.target.dataset.hours);
            loadNews();
        });
    });

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', () => {
        loadMarketData();
        loadNews();
        loadInsight();
    });
}

// Fetch Market Data
async function loadMarketData() {
    const tickerPanel = document.getElementById('ticker-panel');
    tickerPanel.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const tickerHtml = [];

        for (const ticker of TICKERS) {
            try {
                const data = await fetchYahooQuote(ticker.symbol);
                if (data) {
                    const changeClass = data.change >= 0 ? 'ticker-up' : 'ticker-down';
                    const arrow = data.change >= 0 ? '▲' : '▼';

                    tickerHtml.push(`
            <div class="ticker-box">
              <div class="ticker-name">${ticker.name}</div>
              <div class="ticker-price">${data.price}</div>
              <div class="ticker-change ${changeClass}">${arrow} ${data.change.toFixed(2)}%</div>
            </div>
          `);
                }
            } catch (e) {
                console.error(`Error fetching ${ticker.symbol}:`, e);
            }
        }

        tickerPanel.innerHTML = tickerHtml.length > 0 ? tickerHtml.join('') : '<div class="loading">Unable to load market data</div>';
    } catch (error) {
        tickerPanel.innerHTML = '<div class="loading">Error loading data</div>';
    }
}

// Fetch Yahoo Quote
async function fetchYahooQuote(symbol) {
    try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?interval=1d&range=2d`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.chart && data.chart.result && data.chart.result[0]) {
            const result = data.chart.result[0];
            const meta = result.meta;
            const price = meta.regularMarketPrice;
            const prevClose = meta.chartPreviousClose || meta.previousClose;
            const change = ((price - prevClose) / prevClose) * 100;

            return {
                price: price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
                change: change
            };
        }
    } catch (e) {
        console.error('Yahoo fetch error:', e);
    }
    return null;
}

// Load Monthly Insight
async function loadInsight() {
    const insightContent = document.getElementById('insight-content');

    try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/SPY?interval=1d&range=1mo`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.chart && data.chart.result && data.chart.result[0]) {
            const result = data.chart.result[0];
            const closes = result.indicators.quote[0].close;
            const timestamps = result.timestamp;

            let maxChange = 0;
            let maxDate = '';
            let direction = 'up';

            for (let i = 1; i < closes.length; i++) {
                if (closes[i] && closes[i - 1]) {
                    const change = ((closes[i] - closes[i - 1]) / closes[i - 1]) * 100;
                    if (Math.abs(change) > Math.abs(maxChange)) {
                        maxChange = change;
                        maxDate = new Date(timestamps[i] * 1000).toLocaleDateString('en-US');
                        direction = change >= 0 ? 'up' : 'down';
                    }
                }
            }

            const statColor = direction === 'up' ? 'ticker-up' : 'ticker-down';
            const arrow = direction === 'up' ? '▲' : '▼';

            insightContent.innerHTML = `
        <div class="insight-stat ${statColor}">${arrow} ${maxChange.toFixed(2)}%</div>
        <div class="insight-date">on ${maxDate}</div>
        <div class="insight-news">Biggest single-day movement in S&P 500</div>
      `;
        }
    } catch (error) {
        insightContent.innerHTML = '<div class="loading">Unable to load insight</div>';
    }
}

// Load News
async function loadNews() {
    const newsList = document.getElementById('news-list');
    newsList.innerHTML = '<div class="loading">Fetching news...</div>';

    try {
        const allNews = [];

        for (const feedUrl of RSS_FEEDS) {
            try {
                const news = await fetchRSSFeed(feedUrl);
                allNews.push(...news);
            } catch (e) {
                console.error('RSS fetch error:', e);
            }
        }

        // Remove duplicates and sort by hype score
        const uniqueNews = removeDuplicates(allNews);
        const scoredNews = uniqueNews.map(item => ({
            ...item,
            hypeScore: calculateHypeScore(item.title),
            sentiment: analyzeSentiment(item.title)
        }));

        scoredNews.sort((a, b) => b.hypeScore - a.hypeScore);

        // Render top 5 news only
        const topNews = scoredNews.slice(0, 5);

        if (topNews.length > 0) {
            newsList.innerHTML = topNews.map(item => renderNewsItem(item)).join('');
        } else {
            newsList.innerHTML = '<div class="empty-state">No news found. Click Refresh to try again.</div>';
        }
    } catch (error) {
        newsList.innerHTML = '<div class="empty-state">Error loading news</div>';
    }
}

// Fetch RSS Feed with CORS proxy fallback
async function fetchRSSFeed(feedUrl) {
    for (const proxy of CORS_PROXIES) {
        try {
            const response = await fetch(proxy + encodeURIComponent(feedUrl), {
                headers: { 'Accept': 'application/xml, text/xml, */*' }
            });

            if (!response.ok) continue;

            const text = await response.text();
            const parser = new DOMParser();
            const xml = parser.parseFromString(text, 'text/xml');
            const items = xml.querySelectorAll('item');

            if (items.length === 0) continue;

            const news = [];
            items.forEach(item => {
                const title = item.querySelector('title')?.textContent || '';
                const link = item.querySelector('link')?.textContent || '';
                const pubDate = item.querySelector('pubDate')?.textContent || '';
                const source = xml.querySelector('channel > title')?.textContent || 'News';

                if (title) {
                    news.push({
                        title: title.trim(),
                        link: link,
                        date: formatDate(pubDate),
                        source: source.slice(0, 25)
                    });
                }
            });

            if (news.length > 0) return news.slice(0, 8);
        } catch (e) {
            console.error(`Proxy ${proxy} failed:`, e);
            continue;
        }
    }
    return [];
}

// Calculate Hype Score
function calculateHypeScore(title) {
    const titleLower = title.toLowerCase();
    let score = 0;

    HYPE_KEYWORDS.forEach(keyword => {
        if (titleLower.includes(keyword)) score += 10;
    });

    score += (title.match(/!/g) || []).length * 3;
    score += title.split(' ').filter(w => w === w.toUpperCase() && w.length > 2).length * 2;

    return score;
}

// Analyze Sentiment
function analyzeSentiment(title) {
    const titleLower = title.toLowerCase();
    let positiveCount = 0;
    let negativeCount = 0;

    POSITIVE_WORDS.forEach(word => {
        if (titleLower.includes(word)) positiveCount++;
    });

    NEGATIVE_WORDS.forEach(word => {
        if (titleLower.includes(word)) negativeCount++;
    });

    if (positiveCount > negativeCount) return { label: 'Positive', class: 'sentiment-positive', icon: '+' };
    if (negativeCount > positiveCount) return { label: 'Negative', class: 'sentiment-negative', icon: '-' };
    return { label: 'Neutral', class: 'sentiment-neutral', icon: '~' };
}

// Render News Item
function renderNewsItem(item) {
    return `
    <div class="news-item">
      <div class="news-title">${escapeHtml(item.title)}</div>
      <div class="news-meta">
        <span>${item.date}</span>
        <span class="${item.sentiment.class}">[${item.sentiment.icon}] ${item.sentiment.label}</span>
        <span>Hype: ${item.hypeScore}</span>
      </div>
      <div class="news-source">${escapeHtml(item.source)}</div>
      <a href="${item.link}" target="_blank" class="news-link">Visit</a>
    </div>
  `;
}

// Utility Functions
function removeDuplicates(news) {
    const seen = new Set();
    return news.filter(item => {
        if (seen.has(item.title)) return false;
        seen.add(item.title);
        return true;
    });
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch {
        return dateStr.slice(0, 16);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
