import streamlit as st
import joblib
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineScope · Sentiment Analysis",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0b0c10;
    --surface:   #13151c;
    --border:    #1e2130;
    --gold:      #e8c46a;
    --gold-dim:  #a8893a;
    --red:       #e05c5c;
    --green:     #5ce0a0;
    --text:      #d6d8e0;
    --muted:     #6b6e7e;
    --radius:    14px;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Grain overlay ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.2rem, 10vw, 5.5rem);
    letter-spacing: 0.06em;
    line-height: 1;
    color: var(--gold);
    text-shadow: 0 0 60px rgba(232,196,106,0.18);
    margin: 0;
}
.hero-sub {
    font-size: 0.85rem;
    font-weight: 300;
    color: var(--muted);
    margin-top: 0.8rem;
    letter-spacing: 0.04em;
}
.filmstrip {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin: 1.6rem auto 0;
    opacity: 0.35;
}
.filmstrip span {
    display: inline-block;
    width: 18px;
    height: 10px;
    border: 1.5px solid var(--gold-dim);
    border-radius: 2px;
}
.filmstrip span:nth-child(1), .filmstrip span:nth-child(7) { opacity: 0.4; }

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 2rem 1.6rem;
    margin: 1.8rem 0 0;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
    opacity: 0.6;
}
.card-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.75rem;
}

/* ── Text area override ── */
[data-testid="stTextArea"] textarea {
    background: #0e1018 !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    resize: vertical !important;
    padding: 1rem 1.1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold-dim) !important;
    box-shadow: 0 0 0 3px rgba(232,196,106,0.07) !important;
}
[data-testid="stTextArea"] label { display: none; }

/* ── Button ── */
[data-testid="stButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #c9a84c, #e8c46a) !important;
    color: #0b0c10 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.15rem !important;
    letter-spacing: 0.18em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(232,196,106,0.18) !important;
    margin-top: 0.5rem !important;
}
[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

/* ── Result banners ── */
[data-testid="stSuccess"], [data-testid="stError"], [data-testid="stWarning"] {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    margin-top: 1.2rem !important;
    padding: 1rem 1.4rem !important;
    border: none !important;
}
[data-testid="stSuccess"] {
    background: rgba(92,224,160,0.10) !important;
    color: var(--green) !important;
    box-shadow: 0 0 0 1.5px rgba(92,224,160,0.25) !important;
}
[data-testid="stError"] {
    background: rgba(224,92,92,0.10) !important;
    color: var(--red) !important;
    box-shadow: 0 0 0 1.5px rgba(224,92,92,0.25) !important;
}
[data-testid="stWarning"] {
    background: rgba(232,196,106,0.08) !important;
    color: var(--gold) !important;
    box-shadow: 0 0 0 1.5px rgba(232,196,106,0.2) !important;
}

/* ── Divider + footer ── */
[data-testid="stMarkdownContainer"] hr {
    border-color: var(--border) !important;
    margin: 2.2rem 0 1.2rem !important;
}
.footer-note {
    text-align: center;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
.footer-note span {
    color: var(--gold-dim);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Natural Language Processing</div>
    <div class="hero-title">CineScope</div>
    <div class="hero-sub">TF-IDF · Logistic Regression · Sentiment Detection</div>
    <div class="filmstrip">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("sentiment_model.pkl")

# ── Logic ──────────────────────────────────────────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    stop_words = set(ENGLISH_STOP_WORDS)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)

# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">Your Review</div>', unsafe_allow_html=True)
user_input = st.text_area("review_input", placeholder="Write your movie review here…", height=160, label_visibility="collapsed")
predict_clicked = st.button("Analyse Sentiment →")
st.markdown('</div>', unsafe_allow_html=True)

# ── Prediction ─────────────────────────────────────────────────────────────────
if predict_clicked:
    if user_input.strip() != "":
        cleaned = clean_text(user_input)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]
        if prediction == "positive":
            st.success("😊  Positive Sentiment — the audience approves.")
        else:
            st.error("😞  Negative Sentiment — critics aren't impressed.")
    else:
        st.warning("Please enter a review before analysing.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="footer-note">Model loaded from saved file &nbsp;<span>✦</span>&nbsp; Ready to predict</p>', unsafe_allow_html=True)