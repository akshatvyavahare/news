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

# ─── STYLING (WHITE THEME) ───────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #ffffff;
    color: #111111;
  }

  .main .block-container {
    padding: 1rem 2rem;
    max-width: 100%;
  }

  /* Header */
  .terminal-header {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 10px 16px;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
  }

  .terminal-logo {
    font-size: 1.4rem;
    font-weight: 600;
    color: #f59e0b;
  }

  .terminal-time {
    font-size: 0.8rem;
    color: #6b7280;
  }

  /* Sidebar fix */
  section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
  }

  /* Buttons */
  button {
    border-radius: 6px !important;
    border: 1px solid #e5e7eb !important;
    background: #f9fafb !important;
  }

  /* Cards */
  .news-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #f59e0b;
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }

  .news-card:hover {
    background: #f9fafb;
  }

  .news-title {
    font-weight: 600;
    margin-bottom: 5px;
  }

  .news-desc {
    color: #4b5563;
    font-size: 0.9rem;
  }

  .news-source {
    font-size: 0.7rem;
    color: #f59e0b;
    margin-bottom: 5px;
  }

  .news-meta {
    font-size: 0.7rem;
    color: #6b7280;
    display: flex;
    justify-content: space-between;
  }

</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
NEWSAPI_BASE = "https://newsapi.org/v2"

TOPICS = {
    "World": "world",
    "Markets": "stock market",
    "Finance": "finance banking",
    "Tech": "technology AI",
    "Energy": "energy oil gas",
    "Industry": "manufacturing industry",
    "Climate": "climate environment",
    "Politics": "politics government",
    "Science": "science research",
    "Health": "health medicine",
    "Startups": "startup venture capital",
    "Asia": "asia pacific",
}

# ─── API FUNCTIONS ────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_news(api_key, query):
    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": 15,
        "sortBy": "publishedAt",
        "language": "en"
    }
    r = requests.get(f"{NEWSAPI_BASE}/everything", params=params)
    return r.json().get("articles", [])

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def time_ago(published_at):
    try:
        dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        diff = ist_now - dt
        return f"{int(diff.total_seconds()//3600)}h ago"
    except:
        return ""

def render_article(article):
    title = article.get("title", "")
    desc = article.get("description", "")
    source = article.get("source", {}).get("name", "")
    url = article.get("url", "")
    pub = article.get("publishedAt", "")

    st.markdown(f"""
    <div class="news-card">
      <div class="news-source">{source}</div>
      <div class="news-title">{title}</div>
      <div class="news-desc">{desc}</div>
      <div class="news-meta">
        <span>{time_ago(pub)}</span>
        <a href="{url}" target="_blank">Read →</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
st.sidebar.title("Configuration")

api_key = st.secrets.get("NEWS_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter NewsAPI Key", type="password")

# ─── HEADER ──────────────────────────────────────────────────────────────────
ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
now = ist_time.strftime("%Y-%m-%d  %H:%M:%S IST")

st.markdown(f"""
<div class="terminal-header">
  <span class="terminal-logo">NEXUS TERMINAL</span>
  <span class="terminal-time">{now}</span>
</div>
""", unsafe_allow_html=True)

# ─── TOPICS ──────────────────────────────────────────────────────────────────
cols = st.columns(len(TOPICS))

selected_topic = st.session_state.get("topic", "World")

for i, topic in enumerate(TOPICS.keys()):
    if cols[i].button(topic):
        selected_topic = topic
        st.session_state["topic"] = topic

query = TOPICS[selected_topic]

# ─── FETCH DATA ───────────────────────────────────────────────────────────────
if not api_key:
    st.warning("Please enter your NewsAPI key")
    st.stop()

articles = fetch_news(api_key, query)

# ─── DISPLAY ─────────────────────────────────────────────────────────────────
st.subheader(f"{selected_topic} News")

for article in articles:
    render_article(article)

# ─── AUTO REFRESH (optional) ─────────────────────────────────────────────────
# time.sleep(60)
# st.rerun()
