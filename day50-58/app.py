import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import joblib
import re
from urllib.parse import urlparse
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PhishGuard — URL Threat Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #1e1e2e;
}
section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #58a6ff !important; }

/* Main bg */
.main { background: #0b0f1a; }
.block-container { padding-top: 2rem; }

/* Header banner */
.phishguard-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.phishguard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(88,166,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.phishguard-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    color: #58a6ff;
    margin: 0;
    letter-spacing: -1px;
}
.phishguard-header p {
    color: #8b949e;
    font-size: 1rem;
    margin: 0.5rem 0 0;
}

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #58a6ff; }
.metric-card .value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #58a6ff;
}
.metric-card .label {
    font-size: 0.8rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* Result banners */
.result-safe {
    background: linear-gradient(135deg, #0a2a1a, #0d3b24);
    border: 2px solid #238636;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    color: #3fb950;
    font-family: 'Space Mono', monospace;
}
.result-phish {
    background: linear-gradient(135deg, #2a0a0a, #3b0d0d);
    border: 2px solid #da3633;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    color: #f85149;
    font-family: 'Space Mono', monospace;
}
.result-safe h2, .result-phish h2 {
    font-size: 1.6rem;
    margin: 0 0 0.4rem;
}
.result-safe p, .result-phish p {
    margin: 0;
    font-size: 0.85rem;
    opacity: 0.8;
}

/* Feature bar */
.feat-bar-wrap {
    background: #161b22;
    border-radius: 10px;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem 0;
}

/* URL input */
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1.5px solid #21262d !important;
    border-radius: 10px !important;
    color: #c9d1d9 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: #1f6feb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.8rem !important;
    width: 100%;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #388bfd !important; }

/* Tab style */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #21262d !important;
    color: #58a6ff !important;
}

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Section headers */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1.5rem 0 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #21262d;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FEATURE EXTRACTION FROM URL
# ─────────────────────────────────────────────
def extract_url_features(url: str) -> dict:
    """Extract numeric features from a raw URL string."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        path = parsed.path or ""
        query = parsed.query or ""
        full = url

        features = {
            "URLLength":                   len(full),
            "DomainLength":                len(domain),
            "IsDomainIP":                  int(bool(re.match(r'^\d{1,3}(\.\d{1,3}){3}$', domain.replace('www.','')))),
            "URLSimilarityIndex":          0.0,   # requires comparison corpus
            "CharContinuationRate":        _char_continuation(full),
            "TLDLegitimateProb":           _tld_prob(domain),
            "URLCharProb":                 len(re.findall(r'[a-zA-Z0-9]', full)) / max(len(full), 1),
            "TLDLength":                   len(domain.split('.')[-1]) if '.' in domain else 0,
            "NoOfSubDomain":               max(len(domain.split('.')) - 2, 0),
            "HasObfuscation":              int('%' in full or '@' in full),
            "NoOfObfuscatedChar":          full.count('%'),
            "ObfuscationRatio":            full.count('%') / max(len(full), 1),
            "NoOfLettersInURL":            len(re.findall(r'[a-zA-Z]', full)),
            "LetterRatioInURL":            len(re.findall(r'[a-zA-Z]', full)) / max(len(full), 1),
            "NoOfDegitsInURL":             len(re.findall(r'\d', full)),
            "DegitRatioInURL":             len(re.findall(r'\d', full)) / max(len(full), 1),
            "NoOfEqualsInURL":             full.count('='),
            "NoOfQMarkInURL":              full.count('?'),
            "NoOfAmpersandInURL":          full.count('&'),
            "NoOfOtherSpecialCharsInURL":  len(re.findall(r'[^a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]', full)),
            "SpacialCharRatioInURL":       len(re.findall(r'[^a-zA-Z0-9]', full)) / max(len(full), 1),
            "IsHTTPS":                     int(parsed.scheme == 'https'),
            # Page-level features default to neutral values without fetching
            "LineOfCode":                  0,
            "LargestLineLength":           0,
            "HasTitle":                    0,
            "DomainTitleMatchScore":       0.0,
            "URLTitleMatchScore":          0.0,
            "HasFavicon":                  0,
            "Robots":                      0,
            "IsResponsive":                0,
            "NoOfURLRedirect":             0,
            "NoOfSelfRedirect":            0,
            "HasDescription":              0,
            "NoOfPopup":                   0,
            "NoOfiFrame":                  0,
            "HasExternalFormSubmit":       0,
            "HasSocialNet":                0,
            "HasSubmitButton":             0,
            "HasHiddenFields":             0,
            "HasPasswordField":            int('password' in full.lower() or 'login' in full.lower()),
            "Bank":                        int(any(w in full.lower() for w in ['bank','banking','secure','account'])),
            "Pay":                         int(any(w in full.lower() for w in ['pay','payment','checkout','billing'])),
            "Crypto":                      int(any(w in full.lower() for w in ['crypto','bitcoin','wallet','nft'])),
            "HasCopyrightInfo":            0,
            "NoOfImage":                   0,
            "NoOfCSS":                     0,
            "NoOfJS":                      0,
            "NoOfSelfRef":                 0,
            "NoOfEmptyRef":                0,
            "NoOfExternalRef":             0,
        }

        # Engineered features
        features["DigitLetterRatio"]       = features["NoOfDegitsInURL"] / max(features["NoOfLettersInURL"], 1)
        features["TotalSpecialChars"]      = (features["NoOfEqualsInURL"] + features["NoOfQMarkInURL"]
                                               + features["NoOfAmpersandInURL"] + features["NoOfOtherSpecialCharsInURL"])
        features["URLToDomainRatio"]       = features["URLLength"] / max(features["DomainLength"], 1)
        features["HasExternalResources"]   = 0
        features["HasRedirect"]            = 0

        return features
    except Exception as e:
        st.error(f"Feature extraction error: {e}")
        return {}


def _char_continuation(url):
    if len(url) < 2:
        return 0.0
    cont = sum(1 for i in range(1, len(url)) if url[i] == url[i-1])
    return cont / max(len(url) - 1, 1)


def _tld_prob(domain):
    safe_tlds = {'com': 0.52, 'org': 0.45, 'net': 0.43, 'edu': 0.92,
                 'gov': 0.98, 'io': 0.38, 'co': 0.35, 'uk': 0.55, 'de': 0.60}
    parts = domain.split('.')
    tld = parts[-1].lower() if parts else ''
    return safe_tlds.get(tld, 0.15)


# ─────────────────────────────────────────────
#  MODEL LOADER
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        model  = joblib.load("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day50-58/phishing_detector_model.pkl")
        scaler = joblib.load("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day50-58/phishing_detector_scaler.pkl")
        return model, scaler, True
    except FileNotFoundError:
        return None, None, False


# ─────────────────────────────────────────────
#  RISK SCORE HELPER
# ─────────────────────────────────────────────
RISK_FACTORS = {
    "IsHTTPS":           ("Uses HTTPS",           -15, +5),
    "IsDomainIP":        ("IP address as domain",  +30, -2),
    "HasObfuscation":    ("URL obfuscation found",  +25, -2),
    "NoOfSubDomain":     ("Multiple subdomains",    +8,  -1),
    "HasPasswordField":  ("Password keyword in URL",+20, -2),
    "Bank":              ("Banking keyword",        +15, -2),
    "Pay":               ("Payment keyword",        +12, -2),
    "Crypto":            ("Crypto keyword",         +10, -2),
    "URLLength":         None,
    "TLDLegitimateProb": None,
}


def compute_risk_breakdown(feats: dict) -> list:
    items = []
    for key, val in feats.items():
        if key == "URLLength":
            if val > 75:
                items.append(("Long URL (suspicious length)", min((val-75)//10*3, 20), "⚠️"))
            else:
                items.append(("URL length looks normal", -5, "✅"))
        elif key == "TLDLegitimateProb":
            if val < 0.2:
                items.append(("Suspicious TLD", 20, "⚠️"))
            elif val > 0.5:
                items.append(("Trusted TLD", -10, "✅"))
        elif key in RISK_FACTORS and RISK_FACTORS[key]:
            label, risk_if_1, risk_if_0 = RISK_FACTORS[key]
            if val:
                icon = "⚠️" if risk_if_1 > 0 else "✅"
                items.append((label, risk_if_1, icon))
            else:
                if risk_if_0 < 0:
                    items.append((label + " (absent)", risk_if_0, "✅"))
    return items


# ─────────────────────────────────────────────
#  PLOT HELPERS
# ─────────────────────────────────────────────
def dark_fig(figsize=(8, 4)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('#161b22')
    ax.set_facecolor('#0d1117')
    ax.tick_params(colors='#8b949e')
    ax.xaxis.label.set_color('#8b949e')
    ax.yaxis.label.set_color('#8b949e')
    ax.title.set_color('#c9d1d9')
    for spine in ax.spines.values():
        spine.set_edgecolor('#21262d')
    return fig, ax


def plot_confidence_gauge(prob_legit):
    fig, ax = plt.subplots(figsize=(5, 2.8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('#161b22')
    ax.set_facecolor('#161b22')

    theta = np.linspace(0, np.pi, 200)
    # Background arc
    ax.plot(theta, [1]*200, color='#21262d', linewidth=18, solid_capstyle='round')
    # Color arc
    cutoff = int(prob_legit * 200)
    color = '#3fb950' if prob_legit >= 0.6 else '#d29922' if prob_legit >= 0.4 else '#f85149'
    ax.plot(theta[:cutoff], [1]*cutoff, color=color, linewidth=18, solid_capstyle='round')

    # Needle
    angle = np.pi * prob_legit
    ax.annotate("", xy=(angle, 0.95), xytext=(angle, 0.0),
                arrowprops=dict(arrowstyle="-|>", color='white', lw=2, mutation_scale=15))

    ax.set_ylim(0, 1.3)
    ax.set_xlim(0, np.pi)
    ax.axis('off')
    ax.text(np.pi/2, -0.25, f"{prob_legit*100:.1f}%", ha='center', va='center',
            fontsize=22, fontweight='bold', color=color,
            fontfamily='monospace', transform=ax.transData)
    ax.text(np.pi/2, -0.55, "Legitimate Confidence", ha='center', va='center',
            fontsize=9, color='#8b949e', transform=ax.transData)
    plt.tight_layout()
    return fig


def plot_feature_radar(feats):
    categories = [
        'HTTPS', 'No IP Domain', 'No Obfusc.',
        'Short URL', 'Safe TLD', 'No Subdomain'
    ]
    raw_scores = [
        feats.get('IsHTTPS', 0),
        1 - feats.get('IsDomainIP', 0),
        1 - feats.get('HasObfuscation', 0),
        1 - min(feats.get('URLLength', 50) / 120, 1),
        feats.get('TLDLegitimateProb', 0),
        1 - min(feats.get('NoOfSubDomain', 0) / 4, 1),
    ]

    N = len(categories)
    angles = [n / N * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    scores = raw_scores + raw_scores[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#161b22')
    ax.set_facecolor('#0d1117')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9, color='#8b949e')
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%","50%","75%","100%"], size=7, color='#3d444d')
    ax.tick_params(colors='#3d444d')
    for spine in ax.spines.values():
        spine.set_edgecolor('#21262d')
    ax.grid(color='#21262d', linewidth=0.8)

    ax.plot(angles, scores, 'o-', linewidth=2, color='#58a6ff')
    ax.fill(angles, scores, alpha=0.2, color='#58a6ff')
    ax.set_ylim(0, 1)
    ax.set_title('URL Safety Radar', color='#c9d1d9', fontsize=11, pad=20)
    plt.tight_layout()
    return fig


def plot_feature_bars(feats):
    show = {
        'IsHTTPS':           'HTTPS Enabled',
        'URLLength':         'URL Length',
        'NoOfSubDomain':     'Subdomains',
        'HasObfuscation':    'Obfuscation',
        'TLDLegitimateProb': 'TLD Trust',
        'IsDomainIP':        'IP as Domain',
        'NoOfEqualsInURL':   '= Signs',
        'NoOfQMarkInURL':    '? Signs',
        'NoOfAmpersandInURL':'& Signs',
        'DigitLetterRatio':  'Digit/Letter Ratio',
    }
    labels, vals, colors = [], [], []
    for key, name in show.items():
        v = feats.get(key, 0)
        labels.append(name)
        # Normalize for display
        if key == 'URLLength':
            nv = min(v / 120, 1)
        elif key in ('NoOfSubDomain', 'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL'):
            nv = min(v / 5, 1)
        elif key == 'DigitLetterRatio':
            nv = min(v, 1)
        else:
            nv = float(v)
        vals.append(nv)
        bad = key in ('HasObfuscation', 'IsDomainIP', 'URLLength', 'NoOfSubDomain',
                      'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'DigitLetterRatio')
        colors.append('#f85149' if (bad and nv > 0.3) else '#3fb950' if nv > 0.5 else '#d29922')

    fig, ax = dark_fig((7, 4))
    y = range(len(labels))
    bars = ax.barh(y, vals, color=colors, height=0.6, edgecolor='none')
    ax.barh(y, [1]*len(labels), color='#21262d', height=0.6, edgecolor='none', zorder=0)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9, color='#c9d1d9')
    ax.set_xlim(0, 1)
    ax.set_xlabel('Normalized Score', fontsize=9)
    ax.set_title('Feature Analysis', fontsize=11, color='#c9d1d9')
    ax.tick_params(axis='x', colors='#8b949e')
    for bar, val, raw_key in zip(bars, vals, show.keys()):
        raw_v = feats.get(raw_key, 0)
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{raw_v:.2f}' if isinstance(raw_v, float) else str(raw_v),
                va='center', fontsize=8, color='#8b949e')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ PhishGuard")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    PhishGuard uses a machine learning model trained on **235,795 URLs** from the PhiUSIIL dataset.

    **Model Features**
    - 51 engineered URL features
    - Binary classification (Phishing / Legitimate)
    - Confidence score + risk breakdown
    """)

    st.markdown("---")
    st.markdown("### Model Status")
    model, scaler, loaded = load_model()
    if loaded:
        st.success("✅ Model loaded")
        try:
            st.caption(f"Type: `{type(model).__name__}`")
        except:
            pass
    else:
        st.warning("⚠️ Model not found")
        st.caption("Run the notebook first to generate `phishing_detector_model.pkl`")

    st.markdown("---")
    st.markdown("### Quick Test URLs")
    st.code("https://www.google.com", language=None)
    st.code("http://192.168.1.1/login", language=None)
    st.code("https://paypa1-secure.xyz/verify", language=None)

    st.markdown("---")
    st.caption("Built for DS Capstone · PhiUSIIL Dataset")


# ─────────────────────────────────────────────
#  MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="phishguard-header">
  <h1>🛡️ PhishGuard</h1>
  <p>Real-time phishing URL detection powered by machine learning · PhiUSIIL Dataset</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 URL Analyzer", "📊 Model Insights", "📁 Batch Scanner"])


# ════════════════════════════════════════════
#  TAB 1 — URL ANALYZER
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Enter URL to analyze</div>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        url_input = st.text_input(
            "", placeholder="https://example.com/path?query=value",
            label_visibility="collapsed"
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("Analyze →")

    # Sample URLs
    st.markdown('<div class="section-title">Try a sample</div>', unsafe_allow_html=True)
    sample_cols = st.columns(4)
    samples = [
        ("🏦 Fake Bank", "http://secure-bankofamerica.verify-login.net/signin"),
        ("✅ Google",    "https://www.google.com"),
        ("🎮 Gaming",    "https://store.steampowered.com/app/1234"),
        ("💀 Phish",     "http://192.168.0.1/paypal-login/verify?user=admin"),
    ]
    for col, (label, url) in zip(sample_cols, samples):
        with col:
            if st.button(label, key=f"sample_{label}"):
                url_input = url
                analyze = True

    # ── ANALYSIS ──
    if analyze and url_input:
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'http://' + url_input

        with st.spinner("Extracting features & running model..."):
            feats = extract_url_features(url_input)

        if not feats:
            st.error("Could not extract features from this URL.")
        else:
            feat_series = pd.Series(feats)
            feat_df = feat_series.to_frame().T

            # ── MODEL PREDICTION ──
            if loaded:
                try:
                    pred = model.predict(feat_df)[0]
                    prob = model.predict_proba(feat_df)[0]
                    prob_legit = prob[1]
                    prob_phish = prob[0]
                    model_used = True
                except Exception as e:
                    st.warning(f"Model error: {e}. Using heuristic fallback.")
                    model_used = False
            else:
                model_used = False

            if not model_used:
                # Heuristic fallback
                risk = 0
                if not feats.get('IsHTTPS'): risk += 20
                if feats.get('IsDomainIP'):  risk += 35
                if feats.get('HasObfuscation'): risk += 25
                if feats.get('URLLength', 0) > 75: risk += 15
                if feats.get('TLDLegitimateProb', 0.5) < 0.2: risk += 20
                prob_phish = min(risk / 100, 0.99)
                prob_legit = 1 - prob_phish
                pred = 1 if prob_legit >= 0.5 else 0

            st.markdown("---")

            # ── RESULT BANNER ──
            if pred == 1:
                st.markdown(f"""
                <div class="result-safe">
                  <h2>✅ LEGITIMATE URL</h2>
                  <p>Confidence: {prob_legit*100:.1f}% safe · Phishing probability: {prob_phish*100:.1f}%</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-phish">
                  <h2>🚨 PHISHING DETECTED</h2>
                  <p>Confidence: {prob_phish*100:.1f}% malicious · Do NOT visit this URL</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── METRICS ROW ──
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""<div class="metric-card">
                    <div class="value">{prob_legit*100:.1f}%</div>
                    <div class="label">Legit Score</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-card">
                    <div class="value" style="color:#f85149">{prob_phish*100:.1f}%</div>
                    <div class="label">Phish Score</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-card">
                    <div class="value" style="color:#d29922">{feats.get('URLLength',0)}</div>
                    <div class="label">URL Length</div></div>""", unsafe_allow_html=True)
            with m4:
                https_col = '#3fb950' if feats.get('IsHTTPS') else '#f85149'
                st.markdown(f"""<div class="metric-card">
                    <div class="value" style="color:{https_col}">{'Yes' if feats.get('IsHTTPS') else 'No'}</div>
                    <div class="label">HTTPS</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── CHARTS ──
            c1, c2, c3 = st.columns([1.2, 1.2, 1.6])
            with c1:
                st.markdown('<div class="section-title">Confidence Gauge</div>', unsafe_allow_html=True)
                st.pyplot(plot_confidence_gauge(prob_legit), use_container_width=True)
            with c2:
                st.markdown('<div class="section-title">Safety Radar</div>', unsafe_allow_html=True)
                st.pyplot(plot_feature_radar(feats), use_container_width=True)
            with c3:
                st.markdown('<div class="section-title">Feature Breakdown</div>', unsafe_allow_html=True)
                st.pyplot(plot_feature_bars(feats), use_container_width=True)

            # ── RISK FACTORS ──
            st.markdown('<div class="section-title">Risk Factor Breakdown</div>', unsafe_allow_html=True)
            risk_items = compute_risk_breakdown(feats)
            r_cols = st.columns(2)
            for i, (label, score, icon) in enumerate(risk_items):
                with r_cols[i % 2]:
                    bar_color = "#f85149" if score > 0 else "#3fb950"
                    bar_w = min(abs(score) / 30 * 100, 100)
                    st.markdown(f"""
                    <div style="background:#161b22;border:1px solid #21262d;border-radius:8px;
                                padding:0.6rem 1rem;margin:0.25rem 0;display:flex;align-items:center;gap:0.8rem">
                        <span style="font-size:1.1rem">{icon}</span>
                        <div style="flex:1">
                            <div style="font-size:0.82rem;color:#c9d1d9">{label}</div>
                            <div style="background:#21262d;border-radius:4px;height:4px;margin-top:4px">
                                <div style="background:{bar_color};width:{bar_w}%;height:4px;border-radius:4px"></div>
                            </div>
                        </div>
                        <span style="font-family:monospace;font-size:0.8rem;
                                     color:{bar_color}">{'+'if score>0 else ''}{score}</span>
                    </div>""", unsafe_allow_html=True)

            # ── RAW FEATURES TABLE ──
            with st.expander("🔬 View all extracted features"):
                feat_display = pd.DataFrame({
                    'Feature': list(feats.keys()),
                    'Value': list(feats.values())
                })
                st.dataframe(feat_display, use_container_width=True, height=350)


# ════════════════════════════════════════════
#  TAB 2 — MODEL INSIGHTS
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Dataset Overview</div>', unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)
    stats = [
        ("235,795", "Total URLs"),
        ("134,850", "Legitimate"),
        ("100,945", "Phishing"),
        ("51", "Features"),
    ]
    for col, (val, lbl) in zip([d1, d2, d3, d4], stats):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="value">{val}</div>
                <div class="label">{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    # Class distribution
    with col_a:
        st.markdown('<div class="section-title">Class Distribution</div>', unsafe_allow_html=True)
        fig, ax = dark_fig((5, 4))
        sizes = [134850, 100945]
        colors_pie = ['#3fb950', '#f85149']
        wedges, texts, autotexts = ax.pie(
            sizes, labels=['Legitimate', 'Phishing'],
            colors=colors_pie, autopct='%1.1f%%',
            startangle=90, pctdistance=0.8,
            textprops={'color': '#c9d1d9', 'fontsize': 11}
        )
        for at in autotexts:
            at.set_color('white')
            at.set_fontweight('bold')
        ax.set_title('Dataset Label Split', color='#c9d1d9', fontsize=12)
        fig.patch.set_facecolor('#161b22')
        st.pyplot(fig, use_container_width=True)

    # Model comparison
    with col_b:
        st.markdown('<div class="section-title">Model Comparison (F1-Score)</div>', unsafe_allow_html=True)
        model_results = pd.DataFrame({
            'Model': ['Random Forest', 'XGBoost', 'Gradient Boosting',
                      'Decision Tree', 'Logistic Regression', 'KNN'],
            'F1-Score':    [0.9872, 0.9869, 0.9743, 0.9701, 0.9212, 0.9403],
            'ROC-AUC':     [0.9981, 0.9985, 0.9963, 0.9701, 0.9804, 0.9714],
            'Accuracy':    [0.9871, 0.9868, 0.9742, 0.9699, 0.9211, 0.9401],
        })
        fig, ax = dark_fig((5, 4))
        y_pos = range(len(model_results))
        bar_colors = ['#58a6ff' if i == 0 else '#21262d' for i in range(len(model_results))]
        bars = ax.barh(list(y_pos),
                       model_results.sort_values('F1-Score')['F1-Score'],
                       color=plt.cm.Blues(np.linspace(0.3, 0.9, len(model_results))),
                       height=0.6)
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(model_results.sort_values('F1-Score')['Model'], fontsize=9, color='#c9d1d9')
        ax.set_xlim(0.88, 1.0)
        ax.set_xlabel('F1-Score', fontsize=9)
        ax.set_title('Model Comparison', color='#c9d1d9', fontsize=12)
        for bar, val in zip(bars, model_results.sort_values('F1-Score')['F1-Score']):
            ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                    f'{val:.4f}', va='center', fontsize=8, color='#8b949e')
        st.pyplot(fig, use_container_width=True)

    # Feature importance
    st.markdown('<div class="section-title">Feature Importance (Top 15)</div>', unsafe_allow_html=True)
    top_features = pd.DataFrame({
        'Feature': [
            'URLSimilarityIndex', 'TLDLegitimateProb', 'CharContinuationRate',
            'URLCharProb', 'IsHTTPS', 'URLLength', 'HasCopyrightInfo',
            'URLTitleMatchScore', 'NoOfExternalRef', 'DomainTitleMatchScore',
            'LetterRatioInURL', 'NoOfCSS', 'HasSocialNet', 'NoOfJS', 'NoOfImage'
        ],
        'Importance': [
            0.182, 0.143, 0.098, 0.089, 0.076, 0.061, 0.048,
            0.041, 0.038, 0.034, 0.029, 0.025, 0.022, 0.019, 0.016
        ]
    })
    fig, ax = dark_fig((12, 5))
    palette = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(top_features)))[::-1]
    bars = ax.bar(top_features['Feature'], top_features['Importance'],
                  color=palette, edgecolor='none')
    ax.set_xticklabels(top_features['Feature'], rotation=40, ha='right', fontsize=9, color='#c9d1d9')
    ax.set_ylabel('Importance', fontsize=9)
    ax.set_title('Top 15 Feature Importances (Random Forest)', color='#c9d1d9', fontsize=12)
    for bar, val in zip(bars, top_features['Importance']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                f'{val:.3f}', ha='center', fontsize=7, color='#8b949e')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # Metrics table
    st.markdown('<div class="section-title">Full Model Metrics Table</div>', unsafe_allow_html=True)
    st.dataframe(
        model_results.set_index('Model').style
            .background_gradient(cmap='Blues', subset=['F1-Score', 'ROC-AUC', 'Accuracy'])
            .format('{:.4f}'),
        use_container_width=True
    )


# ════════════════════════════════════════════
#  TAB 3 — BATCH SCANNER
# ════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Batch URL Scanner</div>', unsafe_allow_html=True)
    st.markdown("Paste multiple URLs (one per line) or upload a `.txt` / `.csv` file.")

    col_text, col_file = st.columns(2)
    urls_to_scan = []

    with col_text:
        batch_text = st.text_area(
            "Paste URLs here",
            height=200,
            placeholder="https://www.google.com\nhttp://suspicious-site.xyz/login\nhttps://paypal.com"
        )
        if st.button("🔍 Scan Pasted URLs"):
            urls_to_scan = [u.strip() for u in batch_text.strip().split('\n') if u.strip()]

    with col_file:
        uploaded_file = st.file_uploader("Upload .txt or .csv", type=['txt', 'csv'])
        if uploaded_file and st.button("🔍 Scan Uploaded File"):
            content = uploaded_file.read().decode('utf-8', errors='ignore')
            if uploaded_file.name.endswith('.csv'):
                try:
                    df_upload = pd.read_csv(pd.io.common.StringIO(content))
                    url_col = next((c for c in df_upload.columns if 'url' in c.lower()), df_upload.columns[0])
                    urls_to_scan = df_upload[url_col].dropna().tolist()
                except:
                    urls_to_scan = [u.strip() for u in content.split('\n') if u.strip()]
            else:
                urls_to_scan = [u.strip() for u in content.split('\n') if u.strip()]

    if urls_to_scan:
        urls_to_scan = urls_to_scan[:100]  # cap at 100
        st.markdown(f"Scanning **{len(urls_to_scan)}** URLs...")

        progress = st.progress(0)
        batch_results = []

        for i, url in enumerate(urls_to_scan):
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            feats = extract_url_features(url)
            feat_df = pd.Series(feats).to_frame().T

            if loaded:
                try:
                    pred = model.predict(feat_df)[0]
                    prob = model.predict_proba(feat_df)[0]
                    prob_legit = prob[1]
                except:
                    prob_legit = 1 - min((
                        (not feats.get('IsHTTPS', 0)) * 20 +
                        feats.get('IsDomainIP', 0) * 35 +
                        feats.get('HasObfuscation', 0) * 25
                    ) / 100, 0.99)
                    pred = 1 if prob_legit >= 0.5 else 0
            else:
                prob_legit = 1 - min((
                    (not feats.get('IsHTTPS', 0)) * 20 +
                    feats.get('IsDomainIP', 0) * 35 +
                    feats.get('HasObfuscation', 0) * 25
                ) / 100, 0.99)
                pred = 1 if prob_legit >= 0.5 else 0

            batch_results.append({
                'URL':            url[:60] + '...' if len(url) > 60 else url,
                'Prediction':     '✅ Legitimate' if pred == 1 else '🚨 Phishing',
                'Legit %':        f"{prob_legit*100:.1f}%",
                'Phish %':        f"{(1-prob_legit)*100:.1f}%",
                'HTTPS':          '✅' if feats.get('IsHTTPS') else '❌',
                'URL Length':     feats.get('URLLength', 0),
                'Subdomains':     feats.get('NoOfSubDomain', 0),
                'Obfuscated':     '⚠️' if feats.get('HasObfuscation') else '—',
                '_prob_legit':    prob_legit,
            })
            progress.progress((i + 1) / len(urls_to_scan))

        results_df_batch = pd.DataFrame(batch_results)
        n_phish = (results_df_batch['Prediction'].str.contains('Phishing')).sum()
        n_legit = len(results_df_batch) - n_phish

        st.markdown("---")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""<div class="metric-card">
                <div class="value">{len(results_df_batch)}</div>
                <div class="label">URLs Scanned</div></div>""", unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""<div class="metric-card">
                <div class="value" style="color:#3fb950">{n_legit}</div>
                <div class="label">Legitimate</div></div>""", unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""<div class="metric-card">
                <div class="value" style="color:#f85149">{n_phish}</div>
                <div class="label">Phishing</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Distribution plot
        fig, ax = dark_fig((8, 3))
        probs = results_df_batch['_prob_legit'].values
        ax.hist([probs[results_df_batch['Prediction'].str.contains('Legit')],
                 probs[results_df_batch['Prediction'].str.contains('Phish')]],
                bins=20, color=['#3fb950', '#f85149'], label=['Legitimate', 'Phishing'],
                alpha=0.75, stacked=False)
        ax.set_xlabel('Legitimate Confidence Score')
        ax.set_ylabel('Count')
        ax.set_title('Confidence Score Distribution', color='#c9d1d9')
        ax.legend()
        st.pyplot(fig, use_container_width=True)

        # Results table (drop helper col)
        st.dataframe(
            results_df_batch.drop(columns=['_prob_legit']),
            use_container_width=True,
            height=400
        )

        # Download
        csv_out = results_df_batch.drop(columns=['_prob_legit']).to_csv(index=False)
        st.download_button(
            "⬇️ Download Results CSV",
            csv_out,
            file_name="phishguard_results.csv",
            mime="text/csv"
        )