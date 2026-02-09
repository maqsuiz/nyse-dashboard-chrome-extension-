"""
Borsa Haber ve Analiz Uygulaması
NYSE piyasasından son haberleri çeker, hype puanlaması yapar ve duygu analizi ekler.
"""

import streamlit as st
from GoogleNews import GoogleNews
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import urllib.parse

# Sayfa yapılandırması
st.set_page_config(
    page_title="NYSE News Center",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimalist CSS stilleri
st.markdown("""
<style>
    .stApp {
        background: #0a0a0f;
    }
    
    .ticker-panel {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c3 100%);
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .ticker-item {
        text-align: center;
        min-width: 100px;
        padding: 0.3rem 0.5rem;
    }
    
    .ticker-name {
        color: #90caf9;
        font-size: 0.7rem;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    
    .ticker-price {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 700;
    }
    
    .ticker-change {
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    .ticker-up { color: #4caf50; }
    .ticker-down { color: #ef5350; }
    
    .ticker-container {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    
    .ticker-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        text-align: center;
        min-width: 120px;
        flex: 1;
    }
    
    .ticker-box-name {
        color: #9ca3af;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
    }
    
    .ticker-box-price {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .ticker-box-change-up {
        color: #4ade80;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .ticker-box-change-down {
        color: #f87171;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    .news-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #111118;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        border-left: 3px solid #3b82f6;
        transition: all 0.2s ease;
    }
    
    .news-row:hover {
        background: #1a1a24;
        border-left-color: #60a5fa;
    }
    
    .news-content {
        flex: 1;
        padding-right: 1rem;
    }
    
    .news-title {
        color: #e5e7eb;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .news-meta {
        display: flex;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .meta-item {
        color: #6b7280;
        font-size: 0.75rem;
    }
    
    .sentiment-positive { color: #4ade80; }
    .sentiment-negative { color: #f87171; }
    .sentiment-neutral { color: #9ca3af; }
    
    .source-text {
        color: #3b82f6;
        font-size: 0.75rem;
    }
    
    .visit-btn {
        background: #1e40af;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: 500;
        white-space: nowrap;
        transition: background 0.2s ease;
    }
    
    .visit-btn:hover {
        background: #2563eb;
        color: white;
        text-decoration: none;
    }
    
    .stButton > button {
        background: #1e40af;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    .stButton > button:hover {
        background: #2563eb;
    }
    
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .time-filter-label {
        color: #9ca3af;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    
    /* Radio button styling */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    
    .stRadio label {
        background: #111118 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        color: #e5e7eb !important;
        cursor: pointer;
    }
    
    .stRadio label:hover {
        background: #1a1a24 !important;
    }
    
    .insight-panel {
        background: #111118;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    
    .insight-title {
        color: #9ca3af;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #374151;
        padding-bottom: 0.5rem;
    }
    
    .insight-stat {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .insight-label {
        color: #6b7280;
        font-size: 0.75rem;
        margin-bottom: 0.8rem;
    }
    
    .insight-news {
        color: #e5e7eb;
        font-size: 0.8rem;
        line-height: 1.4;
        margin-top: 0.5rem;
    }
    
    .insight-date {
        color: #6b7280;
        font-size: 0.7rem;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

HYPE_KEYWORDS_EN = ['surge', 'crash', 'record', 'breaking', 'soar', 'plunge', 'historic', 
                     'skyrocket', 'collapse', 'boom', 'bust', 'shock', 'alert', 'critical', 'rally']

@st.cache_data(ttl=60)
def get_market_data():
    """Piyasa verilerini çek (1 dakika cache)"""
    try:
        import yfinance as yf
        
        tickers = {
            'GRAM ALTIN': 'GC=F',
            'DOLAR': 'USDTRY=X',
            'EURO': 'EURTRY=X',
            'STERLİN': 'GBPTRY=X',
            'BIST 100': 'XU100.IS',
            'BITCOIN': 'BTC-USD',
            'GÜMÜŞ': 'SI=F'
        }
        
        data = {}
        for name, symbol in tickers.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d')
                if len(hist) >= 1:
                    current = hist['Close'].iloc[-1]
                    if len(hist) >= 2:
                        prev = hist['Close'].iloc[-2]
                        change = ((current - prev) / prev) * 100
                    else:
                        change = 0
                    
                    if name in ['DOLAR', 'EURO', 'STERLİN']:
                        price_str = f"{current:.4f}"
                    elif name == 'BITCOIN':
                        price_str = f"${current:,.0f}"
                    elif name == 'BIST 100':
                        price_str = f"{current:,.2f}"
                    else:
                        price_str = f"{current:.2f}"
                    
                    data[name] = {
                        'price': price_str,
                        'change': change
                    }
            except:
                continue
        
        return data
    except:
        return {}

@st.cache_data(ttl=3600)
def get_monthly_insight():
    """Son 1 ayda en büyük hareket gününü bul"""
    try:
        import yfinance as yf
        from datetime import datetime, timedelta
        
        # S&P 500 verisini çek
        spy = yf.Ticker("SPY")
        hist = spy.history(period="1mo")
        
        if len(hist) < 2:
            return None
        
        # Günlük değişimleri hesapla
        hist['Daily_Change'] = hist['Close'].pct_change() * 100
        
        # En büyük pozitif değişim
        max_idx = hist['Daily_Change'].idxmax()
        max_change = hist['Daily_Change'].loc[max_idx]
        max_date = max_idx.strftime("%Y-%m-%d")
        
        # En büyük negatif değişim
        min_idx = hist['Daily_Change'].idxmin()
        min_change = hist['Daily_Change'].loc[min_idx]
        min_date = min_idx.strftime("%Y-%m-%d")
        
        # Hangi hareket daha büyük?
        if abs(max_change) >= abs(min_change):
            biggest_change = max_change
            biggest_date = max_date
            direction = "up"
        else:
            biggest_change = min_change
            biggest_date = min_date
            direction = "down"
        
        # O gün için haber ara - en fazla 2 haber
        news_list = []
        try:
            import feedparser
            # Yahoo Finance'tan haberler
            rss_url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US'
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:2]:
                title = entry.get('title', '')
                if title:
                    news_list.append(title)
        except:
            pass
        
        # RSS başarısız olduysa GoogleNews dene
        if len(news_list) < 2:
            try:
                googlenews = GoogleNews(lang='en', period='7d')
                googlenews.search('S&P 500 stock market')
                results = googlenews.results()
                for r in results[:2 - len(news_list)]:
                    title = r.get('title', '')
                    if title and title not in news_list:
                        news_list.append(title)
            except:
                pass
        
        if not news_list:
            news_list = ["Market movement recorded"]
        
        return {
            'change': biggest_change,
            'date': biggest_date,
            'direction': direction,
            'news_list': news_list
        }
    except:
        return None

def render_ticker_panel():
    """Üst ticker panelini render et"""
    data = get_market_data()
    
    if not data:
        return
    
    items_html = ""
    for name, info in data.items():
        change = info['change']
        change_class = "ticker-box-change-up" if change >= 0 else "ticker-box-change-down"
        arrow = "▲" if change >= 0 else "▼"
        change_str = f"{arrow} {change:+.2f}%"
        
        items_html += f'<div class="ticker-box"><div class="ticker-box-name">{name}</div><div class="ticker-box-price">{info["price"]}</div><div class="{change_class}">{change_str}</div></div>'
    
    st.markdown(f'<div class="ticker-container">{items_html}</div>', unsafe_allow_html=True)

def calculate_hype_score(title: str) -> int:
    """Haber başlığının hype puanını hesapla"""
    title_lower = title.lower()
    
    score = 0
    for keyword in HYPE_KEYWORDS_EN:
        if keyword in title_lower:
            score += 10
    
    score += title.count('!') * 3
    uppercase_words = len([w for w in title.split() if w.isupper() and len(w) > 2])
    score += uppercase_words * 2
    
    return score

def get_sentiment(text: str) -> tuple:
    """TextBlob ile duygu analizi yap"""
    try:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return ("Positive", "sentiment-positive", "+")
        elif polarity < -0.1:
            return ("Negative", "sentiment-negative", "-")
        else:
            return ("Neutral", "sentiment-neutral", "~")
    except:
        return ("Neutral", "sentiment-neutral", "~")

def clean_url(url: str) -> str:
    """URL'yi temizle ve doğrula"""
    if not url:
        return None
    
    url = str(url).strip()
    
    if url in ['#', '', 'None', 'null', 'javascript:void(0)'] or len(url) < 5:
        return None
    
    if 'news.google.com' in url or 'google.com/url' in url:
        try:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            for key in ['url', 'q', 'u']:
                if key in params and params[key]:
                    url = params[key][0]
                    break
        except:
            pass
    
    if url.startswith('./') or url.startswith('../'):
        return None
    
    if url.startswith('/') and not url.startswith('//'):
        return None
    
    if not url.startswith('http://') and not url.startswith('https://'):
        if url.startswith('//'):
            url = 'https:' + url
        else:
            url = 'https://' + url
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc or '.' not in parsed.netloc:
            return None
        if len(parsed.netloc) < 4:
            return None
    except:
        return None
    
    return url

def get_period_string(hours: int) -> str:
    """Saat değerini GoogleNews period formatına çevir"""
    if hours <= 1:
        return '1h'
    elif hours <= 4:
        return '4h'
    elif hours <= 6:
        return '6h'
    elif hours <= 12:
        return '12h'
    else:
        return '1d'

def fetch_news(keywords: list, hours: int = 24) -> list:
    """GoogleNews ve RSS ile haber çek"""
    all_news = []
    
    # Önce GoogleNews dene
    try:
        period = get_period_string(hours)
        googlenews = GoogleNews(lang='en', period=period)
        
        for keyword in keywords:
            googlenews.clear()
            googlenews.search(keyword)
            results = googlenews.results()
            
            for item in results:
                link = clean_url(item.get('link', ''))
                
                if not link:
                    continue
                
                news_item = {
                    'title': item.get('title', ''),
                    'source': item.get('media', 'Unknown'),
                    'date': item.get('date', ''),
                    'link': link,
                    'desc': item.get('desc', '')
                }
                
                if not news_item['title']:
                    continue
                
                existing_titles = [n['title'] for n in all_news]
                if news_item['title'] not in existing_titles:
                    all_news.append(news_item)
    except Exception as e:
        pass
    
    # GoogleNews başarısız olduysa veya az haber çektiyse RSS dene
    if len(all_news) < 5:
        try:
            import feedparser
            
            rss_feeds = [
                'https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US',
                'https://www.cnbc.com/id/100003114/device/rss/rss.html',
                'https://feeds.marketwatch.com/marketwatch/topstories/',
            ]
            
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:10]:
                        link = clean_url(entry.get('link', ''))
                        if not link:
                            continue
                        
                        # Tarih formatla
                        date_str = ''
                        if hasattr(entry, 'published'):
                            date_str = entry.published[:20] if len(entry.published) > 20 else entry.published
                        
                        news_item = {
                            'title': entry.get('title', ''),
                            'source': feed.feed.get('title', 'RSS Feed'),
                            'date': date_str,
                            'link': link,
                            'desc': entry.get('summary', '')[:200] if entry.get('summary') else ''
                        }
                        
                        if not news_item['title']:
                            continue
                        
                        existing_titles = [n['title'] for n in all_news]
                        if news_item['title'] not in existing_titles:
                            all_news.append(news_item)
                except:
                    continue
        except Exception as e:
            st.warning(f"RSS error: {str(e)}")
    
    if not all_news:
        st.warning("Unable to fetch news. Please try again later.")
    
    return all_news

def process_news(news_list: list) -> list:
    """Haberleri işle: hype puanı ve duygu analizi ekle"""
    processed = []
    
    for news in news_list:
        hype_score = calculate_hype_score(news['title'])
        sentiment_label, sentiment_class, sentiment_icon = get_sentiment(news['title'])
        
        processed.append({
            **news,
            'hype_score': hype_score,
            'sentiment_label': sentiment_label,
            'sentiment_class': sentiment_class,
            'sentiment_icon': sentiment_icon
        })
    
    processed.sort(key=lambda x: x['hype_score'], reverse=True)
    return processed[:10]

def render_news_item(news: dict):
    """Minimalist haber satırı render et"""
    html = f"""
    <div class="news-row">
        <div class="news-content">
            <div class="news-title">{news['title']}</div>
            <div class="news-meta">
                <span class="meta-item">{news['date']}</span>
                <span class="meta-item {news['sentiment_class']}">[{news['sentiment_icon']}] {news['sentiment_label']}</span>
                <span class="meta-item">Hype: {news['hype_score']}</span>
            </div>
            <div class="source-text">{news['source']}</div>
        </div>
        <a href="{news['link']}" target="_blank" class="visit-btn">Visit</a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def main():
    # Ticker paneli
    render_ticker_panel()
    
    st.markdown('<h1 class="main-title">NYSE News Center</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Latest news from Wall Street & US Markets</p>', unsafe_allow_html=True)
    
    # Session state
    if 'nyse_news' not in st.session_state:
        st.session_state.nyse_news = []
    if 'selected_hours' not in st.session_state:
        st.session_state.selected_hours = 24
    
    # Layout: Sol taraf filtreler, sağ taraf haberler
    col_filter, col_news = st.columns([1, 4])
    
    with col_filter:
        st.markdown('<p class="time-filter-label">Time Range</p>', unsafe_allow_html=True)
        
        time_options = {
            "1 Hour": 1,
            "4 Hours": 4,
            "6 Hours": 6,
            "12 Hours": 12,
            "24 Hours": 24
        }
        
        selected = st.radio(
            "Select time range",
            options=list(time_options.keys()),
            index=4,
            label_visibility="collapsed"
        )
        
        new_hours = time_options[selected]
        
        st.markdown("<br>", unsafe_allow_html=True)
        refresh_clicked = st.button("Refresh", use_container_width=True)
        
        # Aylık analiz paneli
        insight = get_monthly_insight()
        if insight:
            if insight['change'] >= 0:
                stat_color = "color: #4ade80;"
                arrow = "▲"
            else:
                stat_color = "color: #f87171;"
                arrow = "▼"
            
            # Haberleri HTML olarak formatla
            news_html = ""
            for news in insight['news_list'][:2]:
                short_news = news[:60] + "..." if len(news) > 60 else news
                news_html += f'<div class="insight-news">• {short_news}</div>'
            
            st.markdown(f'''
            <div class="insight-panel">
                <div class="insight-title">BIGGEST MOVE (30 Days)</div>
                <div class="insight-stat" style="{stat_color}">{arrow} {insight['change']:+.2f}%</div>
                <div class="insight-label">on {insight['date']}</div>
                {news_html}
            </div>
            ''', unsafe_allow_html=True)
        
        # Saat değişti mi kontrol et
        hours_changed = new_hours != st.session_state.selected_hours
        if hours_changed:
            st.session_state.selected_hours = new_hours
    
    with col_news:
        # İlk yükleme veya güncelleme gerekiyorsa
        if not st.session_state.nyse_news or refresh_clicked or hours_changed:
            get_market_data.clear()
            
            with st.spinner(f"Scanning last {st.session_state.selected_hours} hour(s)..."):
                nyse_keywords = ['Stock Market', 'NYSE', 'Wall Street', 'Fed', 'S&P 500', 'Nasdaq']
                nyse_raw = fetch_news(nyse_keywords, hours=st.session_state.selected_hours)
                st.session_state.nyse_news = process_news(nyse_raw)
            
            if hours_changed or refresh_clicked:
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.nyse_news:
            for news in st.session_state.nyse_news:
                render_news_item(news)
        else:
            st.markdown('<div class="empty-state">No news found. Try a different time range or click Refresh.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
