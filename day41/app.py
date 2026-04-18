import streamlit as st
import joblib
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineScope · Review Intelligence",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fraunces:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

:root {
    --bg:           #faf8f3;
    --bg-grad:      radial-gradient(1200px 600px at 80% -10%, #ece7d8 0%, transparent 60%),
                    radial-gradient(900px 500px at -10% 110%, #e8e3f0 0%, transparent 55%),
                    #faf8f3;
    --surface:      #ffffff;
    --surface-2:    #f3f0e8;
    --border:       #e6e0d4;
    --border-soft:  #efeae0;
    --ink:          #14141c;
    --ink-2:        #3a3a48;
    --ink-muted:    #76768a;
    --ink-faint:    #b4b0a8;
    --accent:       #14141c;
    --accent-soft:  #2a2a3d;
    --gold:         #b08a3e;
    --positive:     #0f6b3f;
    --positive-bg:  #e8f4ed;
    --negative:     #a32a1c;
    --negative-bg:  #fbeae6;
    --amber:        #7a5200;
    --amber-bg:     #fbf3dc;
    --radius:       12px;
    --radius-lg:    20px;
    --shadow-sm:    0 1px 2px rgba(20,20,28,0.04), 0 1px 1px rgba(20,20,28,0.03);
    --shadow:       0 4px 24px -8px rgba(20,20,28,0.10), 0 2px 6px -2px rgba(20,20,28,0.05);
    --shadow-lg:    0 24px 48px -16px rgba(20,20,28,0.18), 0 8px 16px -8px rgba(20,20,28,0.08);
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-grad) !important;
    background-attachment: fixed !important;
    color: var(--ink);
    font-family: 'Inter', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], [data-testid="stToolbar"] { display: none; }

[data-testid="stMainBlockContainer"] {
    padding-top: 3.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 720px !important;
}

/* ── Header pill ── */
.header-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(20,20,28,0.92);
    backdrop-filter: blur(8px);
    color: #fafaf7;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 7px 16px 7px 12px;
    border-radius: 100px;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-sm);
}
.header-pill .live-dot {
    width: 7px;
    height: 7px;
    background: #6ee7b7;
    border-radius: 50%;
    box-shadow: 0 0 0 3px rgba(110,231,183,0.25);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 3px rgba(110,231,183,0.25); }
    50%      { box-shadow: 0 0 0 6px rgba(110,231,183,0.05); }
}

/* ── Hero ── */
.hero { padding: 0 0 2rem; }
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: clamp(2.8rem, 7vw, 4.4rem);
    font-weight: 600;
    letter-spacing: -0.035em;
    line-height: 1.02;
    color: var(--ink);
    margin: 0 0 1.1rem;
}
.hero-title .accent {
    font-style: italic;
    font-weight: 400;
    color: var(--gold);
}
.hero-desc {
    font-size: 1rem;
    font-weight: 300;
    color: var(--ink-2);
    line-height: 1.7;
    max-width: 520px;
    margin: 0;
}
.hero-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--border) 0%, transparent 100%);
    margin: 2.2rem 0 2rem;
}

/* ── Tags ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1.4rem; }
.tag {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--ink-2);
    background: rgba(255,255,255,0.6);
    border: 1px solid var(--border);
    padding: 5px 11px;
    border-radius: 100px;
    letter-spacing: 0.03em;
    backdrop-filter: blur(4px);
}

/* ── Panel ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: var(--radius-lg);
    padding: 1.8rem 1.9rem 1.5rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gold) 0%, var(--accent) 60%, transparent 100%);
    opacity: 0.85;
}
.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1rem;
}
.panel-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink-muted);
}
.panel-hint {
    font-size: 0.72rem;
    color: var(--ink-faint);
    font-weight: 400;
}

/* ── Text area ── */
[data-testid="stTextArea"] textarea {
    background: var(--surface-2) !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius) !important;
    color: var(--ink) !important;
    font-family: 'Fraunces', serif !important;
    font-size: 1.02rem !important;
    font-weight: 400 !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    padding: 1.1rem 1.3rem !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 1px 2px rgba(20,20,28,0.03) !important;
}
[data-testid="stTextArea"] textarea:focus {
    background: #fff !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(20,20,28,0.06), inset 0 1px 2px rgba(20,20,28,0.02) !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: var(--ink-faint) !important;
    font-style: italic;
}
[data-testid="stTextArea"] label { display: none; }

/* ── Button ── */
[data-testid="stButton"] button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #fafaf7 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    border: 1px solid var(--accent) !important;
    border-radius: var(--radius) !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(.4,0,.2,1) !important;
    margin-top: 1rem !important;
    box-shadow: 0 1px 2px rgba(20,20,28,0.08), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
[data-testid="stButton"] button:hover {
    background: var(--accent-soft) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stButton"] button:active { transform: translateY(0) !important; }

/* ── Result cards ── */
.result-card {
    margin-top: 1.5rem;
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    border: 1px solid;
    animation: slideUp 0.45s cubic-bezier(.2,.7,.3,1);
    box-shadow: var(--shadow-sm);
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card.positive {
    background: var(--positive-bg);
    border-color: rgba(15,107,63,0.18);
    color: var(--positive);
}
.result-card.negative {
    background: var(--negative-bg);
    border-color: rgba(163,42,28,0.18);
    color: var(--negative);
}
.result-card.warning {
    background: var(--amber-bg);
    border-color: rgba(122,82,0,0.18);
    color: var(--amber);
}
.result-head {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}
.result-icon {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    background: rgba(255,255,255,0.55);
}
.result-body {
    font-size: 0.9rem;
    font-weight: 400;
    line-height: 1.55;
    opacity: 0.85;
    font-family: 'Inter', sans-serif;
}

/* Confidence bar */
.conf-wrap { margin-top: 14px; }
.conf-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 6px;
    opacity: 0.75;
    font-family: 'Inter', sans-serif;
}
.conf-track {
    height: 6px;
    background: rgba(255,255,255,0.55);
    border-radius: 100px;
    overflow: hidden;
}
.conf-fill {
    height: 100%;
    border-radius: 100px;
    background: currentColor;
    opacity: 0.75;
    animation: grow 0.8s cubic-bezier(.2,.7,.3,1);
    transform-origin: left;
}
@keyframes grow {
    from { transform: scaleX(0); }
    to   { transform: scaleX(1); }
}

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    color: var(--ink-faint);
    letter-spacing: 0.04em;
}
.footer-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6ee7b7;
    box-shadow: 0 0 0 3px rgba(110,231,183,0.2);
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink-faint); }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="header-pill">
        <span class="live-dot"></span>
        Sentiment Engine · Live
    </div>
    <h1 class="hero-title">CineScope<br><span class="accent">review intelligence.</span></h1>
    <p class="hero-desc">
        Paste any movie review and our model instantly classifies its sentiment —
        trained on thousands of real audience critiques and refined for nuance.
    </p>
    <div class="tag-row">
        <span class="tag">TF-IDF Vectoriser</span>
        <span class="tag">Logistic Regression</span>
        <span class="tag">Natural Language Processing</span>
    </div>
</div>
<div class="hero-rule"></div>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
vectorizer = joblib.load("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day41/tfidf_vectorizer.pkl")
model = joblib.load("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day41/sentiment_model.pkl")

# ── Logic ──────────────────────────────────────────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(ENGLISH_STOP_WORDS)
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words)

# ── Input panel ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="panel">
    <div class="panel-header">
        <span class="panel-label">Your Review</span>
        <span class="panel-hint">English · any length</span>
    </div>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area(
    "review_input",
    placeholder="“A breathtaking journey from start to finish — the cinematography alone is worth the ticket…”",
    height=170,
    label_visibility="collapsed",
)
predict_clicked = st.button("Analyse Sentiment  →")

# ── Prediction ─────────────────────────────────────────────────────────────────
if predict_clicked:
    if user_input.strip() != "":
        cleaned = clean_text(user_input)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]

        # Try to get probability for confidence meter
        confidence = None
        try:
            proba = model.predict_proba(vectorized)[0]
            confidence = float(max(proba)) * 100
        except Exception:
            pass

        conf_html = ""
        if confidence is not None:
            conf_html = f"""
            <div class="conf-wrap">
                <div class="conf-label">
                    <span>Model Confidence</span><span>{confidence:.1f}%</span>
                </div>
                <div class="conf-track">
                    <div class="conf-fill" style="width:{confidence:.1f}%"></div>
                </div>
            </div>"""

        if str(prediction).lower() == "positive":
            st.markdown(f"""
            <div class="result-card positive">
                <div class="result-head">
                    <span class="result-icon">★</span>
                    Positive Sentiment
                </div>
                <div class="result-body">The audience approves — this review carries warmth and praise.</div>
                {conf_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card negative">
                <div class="result-head">
                    <span class="result-icon">✕</span>
                    Negative Sentiment
                </div>
                <div class="result-body">Critics aren't impressed — the tone leans toward disappointment.</div>
                {conf_html}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card warning">
            <div class="result-head">
                <span class="result-icon">!</span>
                No Review Provided
            </div>
            <div class="result-body">Please enter a review above before analysing.</div>
        </div>""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span class="footer-status"><span class="status-dot"></span>Model loaded · Ready to predict</span>
    <span>CineScope · v1.0</span>
</div>
""", unsafe_allow_html=True)
