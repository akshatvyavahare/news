import streamlit as st
import requests
from datetime import datetime, timedelta
import time

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS | News Terminal",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── STYLING ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

  /* Base */
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0a0c10;
    color: #c8d0d9;
  }
  .main .block-container { padding: 0.5rem 1.5rem 2rem; max-width: 100%; }

  /* Terminal header */
  .terminal-header {
    background: #0d1117;
    border-bottom: 1px solid #f5a623;
    padding: 10px 16px;
    margin: -0.5rem -1.5rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .terminal-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: #f5a623;
    letter-spacing: 0.12em;
  }
  .terminal-time {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #5c6370;
  }
  .terminal-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #3fb950;
    border: 1px solid #3fb950;
    padding: 2px 8px;
    border-radius: 2px;
  }

  /* Topic pill buttons */
  div[data-testid="column"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: #161b22 !important;
    color: #8b949e !important;
    border: 1px solid #30363d !important;
    border-radius: 2px !important;
    padding: 4px 12px !important;
    width: 100% !important;
    transition: all 0.15s !important;
  }
  div[data-testid="column"] button:hover {
    background: #21262d !important;
    color: #f5a623 !important;
    border-color: #f5a623 !important;
  }

  /* News cards */
  .news-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-left: 3px solid #f5a623;
    border-radius: 2px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: border-color 0.15s;
    cursor: pointer;
  }
  .news-card:hover { border-left-color: #58a6ff; background: #111820; }
  .news-card-breaking { border-left-color: #f85149 !important; }
  .news-card-positive { border-left-color: #3fb950 !important; }
  .news-card-neutral  { border-left-color: #8b949e !important; }

  .news-source {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #f5a623;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .news-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: #e6edf3;
    line-height: 1.4;
    margin-bottom: 6px;
  }
  .news-desc {
    font-size: 0.80rem;
    color: #8b949e;
    line-height: 1.5;
    margin-bottom: 8px;
  }
  .news-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #484f58;
    display: flex;
    justify-content: space-between;
  }
  .news-link {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #58a6ff;
    text-decoration: none;
  }

  /* Section labels */
  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #484f58;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid #21262d;
    padding-bottom: 6px;
    margin-bottom: 14px;
    margin-top: 1rem;
  }

  /* Stats bar */
  .stats-bar {
    display: flex;
    gap: 24px;
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 2px;
    padding: 10px 16px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  .stat-item { text-align: center; }
  .stat-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: #f5a623;
  }
  .stat-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #484f58;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  /* Ticker tape */
  .ticker-wrap {
    background: #0d1117;
    border-top: 1px solid #21262d;
    border-bottom: 1px solid #21262d;
    overflow: hidden;
    padding: 6px 0;
    margin: 0 -1.5rem 1.5rem;
  }
  .ticker-inner {
    display: flex;
    gap: 40px;
    animation: ticker-scroll 40s linear infinite;
    white-space: nowrap;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
  }
  .ticker-item { color: #8b949e; }
  .ticker-item span { color: #3fb950; margin-left: 4px; }
  .ticker-item.neg span { color: #f85149; }
  @keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d;
  }
  [data-testid="stSidebar"] .stTextInput input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    border-radius: 2px !important;
  }
  [data-testid="stSidebar"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #8b949e !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
  }
  [data-testid="stSidebar"] .stSelectbox select {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-size: 0.8rem !important;
  }
  [data-testid="stSidebar"] .stSlider > div { padding: 0 !important; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #f5a623 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 600 !important;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; background: #0a0c10; }
  ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 2px; }

  /* Hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
  [data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── CONSTANTS ───────────────────────────────────────────────────────────────
NEWSAPI_BASE = "https://newsapi.org/v2"
TOPICS = {
    "🌐 World":       "world",
    "💹 Markets":     "stock market",
    "🏦 Finance":     "finance banking",
    "💻 Technology":  "technology AI",
    "⚡ Energy":      "energy oil gas",
    "🏭 Industry":    "manufacturing industry",
    "🌿 Climate":     "climate environment",
    "🏛️ Politics":    "politics government",
    "🔬 Science":     "science research",
    "🩺 Health":      "health medicine",
    "🚀 Startups":    "startup venture capital",
    "🌏 Asia":        "asia pacific",
}
SORT_OPTIONS = {
    "⏱ Latest":      "publishedAt",
    "🔥 Relevance":  "relevancy",
    "📈 Popularity": "popularity",
}


# ─── API FUNCTIONS ────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_news(api_key, query, sort_by="publishedAt", page_size=30, from_date=None, language="en"):
    params = {
        "q": query,
        "apiKey": api_key,
        "sortBy": sort_by,
        "pageSize": page_size,
        "language": language,
    }
    if from_date:
        params["from"] = from_date
    try:
        r = requests.get(f"{NEWSAPI_BASE}/everything", params=params, timeout=10)
        data = r.json()
        if data.get("status") == "ok":
            return data.get("articles", []), None
        return [], data.get("message", "API error")
    except Exception as e:
        return [], str(e)


@st.cache_data(ttl=300)
def fetch_top_headlines(api_key, category="general", country="us"):
    params = {
        "apiKey": api_key,
        "category": category,
        "country": country,
        "pageSize": 10,
    }
    try:
        r = requests.get(f"{NEWSAPI_BASE}/top-headlines", params=params, timeout=10)
        data = r.json()
        if data.get("status") == "ok":
            return data.get("articles", [])
        return []
    except:
        return []


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def time_ago(published_at):
    if not published_at:
        return "—"
    try:
        dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        diff = datetime.utcnow() - dt
        s = int(diff.total_seconds())
        if s < 60:   return f"{s}s ago"
        if s < 3600: return f"{s//60}m ago"
        if s < 86400: return f"{s//3600}h ago"
        return f"{s//86400}d ago"
    except:
        return "—"


def card_class(title):
    title = (title or "").lower()
    if any(w in title for w in ["crash", "crisis", "war", "attack", "breaking", "alert", "urgent", "disaster"]):
        return "news-card news-card-breaking"
    if any(w in title for w in ["surge", "record", "growth", "rally", "rise", "gain", "profit", "boom"]):
        return "news-card news-card-positive"
    if any(w in title for w in ["fall", "drop", "decline", "loss", "cut"]):
        return "news-card news-card-neutral"
    return "news-card"


def render_article(article):
    title   = article.get("title") or "No title"
    desc    = article.get("description") or ""
    source  = article.get("source", {}).get("name") or "Unknown"
    url     = article.get("url") or "#"
    pub     = article.get("publishedAt", "")
    author  = article.get("author") or ""

    if title == "[Removed]":
        return

    cls = card_class(title)
    author_str = f" · {author[:40]}" if author else ""

    st.markdown(f"""
    <div class="{cls}">
      <div class="news-source">{source}</div>
      <div class="news-title">{title}</div>
      {'<div class="news-desc">' + desc[:200] + ('…' if len(desc) > 200 else '') + '</div>' if desc else ''}
      <div class="news-meta">
        <span>{time_ago(pub)}{author_str}</span>
        <a class="news-link" href="{url}" target="_blank">READ FULL STORY →</a>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Configuration")
    api_key = st.secrets.get("NEWS_API_KEY", "")
    
    st.markdown("### 📡 Feed Settings")
    sort_label = st.selectbox("Sort by", list(SORT_OPTIONS.keys()))
    sort_by    = SORT_OPTIONS[sort_label]

    date_range = st.slider("Days back", min_value=1, max_value=30, value=3)
    page_size  = st.slider("Articles per topic", min_value=5, max_value=50, value=15)

    language   = st.selectbox("Language", ["en", "de", "fr", "es", "it", "pt", "ar", "zh"], index=0)
    country    = st.selectbox("Headline country", ["us", "gb", "in", "au", "ca", "de", "fr", "jp"], index=0)

    st.markdown("### 🔍 Custom Search")
    custom_query = st.text_input("Search query", placeholder="e.g. NVIDIA earnings…")

    st.markdown("### 🔄 Auto-refresh")
    auto_refresh = st.toggle("Enable auto-refresh", value=False)
    if auto_refresh:
        refresh_interval = st.slider("Interval (seconds)", 30, 300, 60)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#484f58;line-height:1.8;">
    NEXUS TERMINAL v1.0<br>
    DATA: NewsAPI.org<br>
    CACHE: 5 MIN TTL<br>
    </div>
    """, unsafe_allow_html=True)


# ─── HEADER ──────────────────────────────────────────────────────────────────
now = datetime.utcnow().strftime("%Y-%m-%d  %H:%M:%S UTC")
st.markdown(f"""
<div class="terminal-header">
  <span class="terminal-logo">◈ NEXUS TERMINAL</span>
  <span class="terminal-time">{now}</span>
  <span class="terminal-status">● LIVE</span>
</div>
""", unsafe_allow_html=True)

# ─── GUARD: API KEY ───────────────────────────────────────────────────────────
if not api_key:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;font-family:'IBM Plex Mono',monospace;">
      <div style="font-size:2.5rem;color:#f5a623;margin-bottom:1rem;">◈</div>
      <div style="font-size:1.1rem;color:#e6edf3;margin-bottom:0.5rem;font-weight:500;">NEXUS TERMINAL</div>
      <div style="font-size:0.8rem;color:#8b949e;margin-bottom:2rem;">Real-time news intelligence dashboard</div>
      <div style="font-size:0.75rem;color:#484f58;border:1px solid #21262d;display:inline-block;padding:12px 24px;border-radius:2px;">
        Enter your NewsAPI key in the sidebar to begin.<br>
        Get a free key at <span style="color:#58a6ff;">newsapi.org</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── TOPIC BAR ───────────────────────────────────────────────────────────────
if "active_topic" not in st.session_state:
    st.session_state.active_topic = "🌐 World"
if "custom_mode" not in st.session_state:
    st.session_state.custom_mode = False

topic_keys = list(TOPICS.keys())
cols = st.columns(len(topic_keys))
for i, topic in enumerate(topic_keys):
    if cols[i].button(topic, key=f"topic_{i}"):
        st.session_state.active_topic = topic
        st.session_state.custom_mode  = False


# ─── DETERMINE QUERY ─────────────────────────────────────────────────────────
if custom_query:
    active_query = custom_query
    display_label = f"Search: {custom_query}"
    st.session_state.custom_mode = True
else:
    active_query  = TOPICS[st.session_state.active_topic]
    display_label = st.session_state.active_topic

from_date = (datetime.utcnow() - timedelta(days=date_range)).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─── FETCH DATA ───────────────────────────────────────────────────────────────
with st.spinner(""):
    articles, error = fetch_news(
        api_key, active_query, sort_by=sort_by,
        page_size=page_size, from_date=from_date, language=language
    )
    headlines = fetch_top_headlines(api_key, country=country)


# ─── TICKER TAPE ─────────────────────────────────────────────────────────────
if headlines:
    ticker_items = ""
    for h in (headlines * 2):  # duplicate for infinite scroll illusion
        t = (h.get("title") or "")[:80]
        src = h.get("source", {}).get("name", "")
        ticker_items += f'<span class="ticker-item">[{src}] {t} <span>●</span></span>'

    st.markdown(f"""
    <div class="ticker-wrap">
      <div class="ticker-inner">{ticker_items}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── STATS BAR ───────────────────────────────────────────────────────────────
total = len(articles)
sources = len(set(a.get("source", {}).get("name", "") for a in articles))
oldest = min((a.get("publishedAt","") for a in articles), default="—")
oldest_fmt = oldest[:10] if oldest != "—" else "—"

st.markdown(f"""
<div class="stats-bar">
  <div class="stat-item"><div class="stat-val">{total}</div><div class="stat-lbl">Articles</div></div>
  <div class="stat-item"><div class="stat-val">{sources}</div><div class="stat-lbl">Sources</div></div>
  <div class="stat-item"><div class="stat-val">{date_range}D</div><div class="stat-lbl">Time window</div></div>
  <div class="stat-item"><div class="stat-val">{oldest_fmt}</div><div class="stat-lbl">Earliest</div></div>
  <div class="stat-item"><div class="stat-val">{sort_label.split()[1]}</div><div class="stat-lbl">Sort mode</div></div>
</div>
""", unsafe_allow_html=True)


# ─── ERROR HANDLING ───────────────────────────────────────────────────────────
if error:
    st.markdown(f"""
    <div style="background:#1a0a0a;border:1px solid #f85149;border-radius:2px;padding:12px 16px;
                font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#f85149;margin-bottom:1rem;">
      ⚠ API ERROR: {error}
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN LAYOUT: 2 COLUMNS ──────────────────────────────────────────────────
col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown(f'<div class="section-label">// {display_label} · {total} results</div>', unsafe_allow_html=True)

    if not articles:
        st.markdown("""
        <div style="padding:2rem;text-align:center;font-family:'IBM Plex Mono',monospace;
                    font-size:0.8rem;color:#484f58;border:1px solid #21262d;border-radius:2px;">
          NO DATA — CHECK API KEY OR ADJUST FILTERS
        </div>
        """, unsafe_allow_html=True)
    else:
        for article in articles:
            render_article(article)

with col_side:
    st.markdown('<div class="section-label">// TOP HEADLINES</div>', unsafe_allow_html=True)
    if headlines:
        for article in headlines:
            render_article(article)
    else:
        st.markdown("""
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#484f58;padding:1rem;">
          NO HEADLINES AVAILABLE
        </div>
        """, unsafe_allow_html=True)

    # Source breakdown
    if articles:
        st.markdown('<div class="section-label" style="margin-top:2rem;">// SOURCE BREAKDOWN</div>', unsafe_allow_html=True)
        src_counts = {}
        for a in articles:
            src = a.get("source", {}).get("name") or "Unknown"
            src_counts[src] = src_counts.get(src, 0) + 1
        top_sources = sorted(src_counts.items(), key=lambda x: -x[1])[:10]
        for src, count in top_sources:
            pct = int(count / total * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            st.markdown(f"""
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;margin-bottom:6px;">
              <span style="color:#8b949e;">{src[:22]:<22}</span>
              <span style="color:#f5a623;">{bar}</span>
              <span style="color:#484f58;"> {count}</span>
            </div>
            """, unsafe_allow_html=True)


# ─── AUTO REFRESH ─────────────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(refresh_interval)
    st.cache_data.clear()
    st.rerun()
