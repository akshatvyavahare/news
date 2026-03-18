import streamlit as st
import requests
from datetime import datetime, timedelta

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SAFE LIGHT STYLING (NO BREAKING SELECTORS) ──────────────
st.markdown("""
<style>
body {
    background-color: #ffffff;
    color: #111111;
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

.logo {
    font-size: 22px;
    font-weight: 600;
    color: #f59e0b;
}

.time {
    font-size: 14px;
    color: #6b7280;
}

/* Cards */
.card {
    border: 1px solid #e5e7eb;
    border-left: 4px solid #f59e0b;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    background: #ffffff;
}

.card:hover {
    background: #f9fafb;
}

.title {
    font-weight: 600;
    margin-bottom: 6px;
}

.desc {
    font-size: 14px;
    color: #4b5563;
}

.meta {
    font-size: 12px;
    color: #6b7280;
    display: flex;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────
NEWSAPI_BASE = "https://newsapi.org/v2"

TOPICS = {
    "World": "world",
    "Markets": "stock market",
    "Finance": "finance banking",
    "Technology": "technology AI",
    "Energy": "energy oil gas",
    "Industry": "manufacturing industry",
    "Climate": "climate environment",
    "Politics": "politics government",
    "Science": "science research",
    "Health": "health medicine",
    "Startups": "startup venture capital",
    "Asia": "asia pacific",
}

# ─── API ───────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_news(api_key, query):
    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": 15,
        "sortBy": "publishedAt",
        "language": "en"
    }
    try:
        res = requests.get(f"{NEWSAPI_BASE}/everything", params=params, timeout=10)
        return res.json().get("articles", [])
    except:
        return []

# ─── HELPERS ───────────────────────────────────────────────
def time_ago(published_at):
    try:
        dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        diff = ist_now - dt
        hours = int(diff.total_seconds() // 3600)
        return f"{hours}h ago"
    except:
        return ""

def render_card(article):
    title = article.get("title", "")
    desc = article.get("description", "")
    source = article.get("source", {}).get("name", "")
    url = article.get("url", "")
    pub = article.get("publishedAt", "")

    st.markdown(f"""
    <div class="card">
        <div style="font-size:12px;color:#f59e0b;margin-bottom:4px;">{source}</div>
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
        <div class="meta">
            <span>{time_ago(pub)}</span>
            <a href="{url}" target="_blank">Read →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR (WORKING) ─────────────────────────────────────
st.sidebar.title("Configuration")

api_key = st.secrets.get("NEWS_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter NewsAPI Key", type="password")

# ─── HEADER (IST TIME) ─────────────────────────────────────
ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)

st.markdown(f"""
<div class="header">
    <div class="logo">NEXUS TERMINAL</div>
    <div class="time">{ist_time.strftime("%Y-%m-%d %H:%M:%S IST")}</div>
</div>
""", unsafe_allow_html=True)

# ─── TOPIC SELECTOR ────────────────────────────────────────
if "topic" not in st.session_state:
    st.session_state.topic = "World"

cols = st.columns(len(TOPICS))

for i, topic in enumerate(TOPICS.keys()):
    if cols[i].button(topic):
        st.session_state.topic = topic

selected_topic = st.session_state.topic
query = TOPICS[selected_topic]

# ─── FETCH DATA ───────────────────────────────────────────
if not api_key:
    st.warning("Please enter your NewsAPI key")
    st.stop()

articles = fetch_news(api_key, query)

# ─── DISPLAY ──────────────────────────────────────────────
st.subheader(f"{selected_topic} News")

if not articles:
    st.info("No articles found")
else:
    for article in articles:
        render_card(article)
