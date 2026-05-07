# 🛡️ PhishGuard — Phishing URL Detection

> **Day 50–58 | 60-Days Global Coding Challenge · AB Talks**  
> An end-to-end Data Science Capstone: from raw data to an interactive ML-powered web app.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Dataset](https://img.shields.io/badge/Dataset-PhiUSIIL-blue?style=flat)](https://archive.ics.uci.edu/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Why This Model Matters](#-why-this-model-matters)
- [What the Model Outputs](#-what-the-model-outputs)
- [Live Demo](#-live-demo)
- [Project Pipeline](#-project-pipeline)
- [Dataset](#-dataset)
- [Model Results](#-model-results)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Running the Notebook](#-running-the-notebook)
- [Running the Web App](#-running-the-web-app)
- [Feature Engineering](#-feature-engineering)
- [Tech Stack](#-tech-stack)
- [Key Insights](#-key-insights)
- [Author](#-author)

---

## 🔍 Overview

**PhishGuard** is a complete, production-style Data Science project that detects phishing URLs using machine learning. Built as part of the **60-Days Global Coding Challenge (Days 50–58)**, it covers every stage of a real-world ML pipeline:

| Stage | What was done |
|---|---|
| **Data Understanding** | Explored 235,795 URLs with 56 features |
| **EDA** | Class distributions, correlations, feature distributions by class |
| **Preprocessing** | Null handling, column drops, stratified splits, scaling |
| **Feature Engineering** | 5 derived features (digit-letter ratio, special char counts, etc.) |
| **Modelling** | Trained & compared 6 ML classifiers with 5-fold CV |
| **Evaluation** | Accuracy, F1, Precision, Recall, ROC-AUC, Confusion Matrix |
| **Tuning** | GridSearchCV hyperparameter optimization |
| **Deployment** | Interactive Streamlit web app with real-time URL analysis |

---

## 🎯 Why This Model Matters

### The Real-World Problem

Phishing is one of the most prevalent and damaging forms of cybercrime. Attackers craft URLs that look deceptively similar to trusted websites — mimicking banks, payment portals, or social media platforms — to steal credentials, financial data, and personal information.

Over **3.4 billion phishing emails** are sent every day, and phishing accounts for more than **36% of all data breaches**. Traditional blacklist-based defences (blocking known bad URLs) fail against newly registered phishing domains, which can be deployed and abandoned within hours — long before any blocklist catches up.

### Why Machine Learning?

Rule-based systems ("flag any URL with more than 3 subdomains") are rigid and easy to evade. A machine learning model trained on 235,795 real URLs learns **complex, non-obvious patterns** that no hand-written rule set can capture — for example, the relationship between a TLD's legitimacy score, character continuation rate, and URL-to-domain length ratio acting *together* as a composite phishing signal.

PhishGuard addresses this gap by learning directly from data, making it:

- **Adaptive** — can be retrained as attacker tactics evolve
- **Scalable** — analyses any URL in milliseconds
- **Interpretable** — surfaces which features drove each prediction
- **Generalizable** — detects threats on URLs it has never seen before

### Who Benefits?

| Audience | Use Case |
|---|---|
| **Security Teams** | Integrate into email gateways or browser extensions to auto-flag suspicious links |
| **End Users** | Paste a URL into the app before clicking an unfamiliar link |
| **Developers** | Use the exported `.pkl` model as a microservice in any Python backend |
| **Researchers** | Extend the feature set or swap in new classifiers for benchmarking |

---

## 📤 What the Model Outputs

For every URL submitted, the model produces the following:

### 1. Binary Prediction — The Verdict

The primary output is a classification label:

| Output | Label | Meaning | Recommended Action |
|---|---|---|---|
| ✅ **Legitimate** | `1` | URL shows patterns consistent with safe, genuine websites | Safe to visit |
| 🚨 **Phishing** | `0` | URL shows patterns associated with malicious or deceptive sites | Do NOT visit |

### 2. Confidence Score — How Certain Is the Model?

The model returns a **probability between 0% and 100%** for each class, not just a hard label. This tells you *how strongly* the model believes its verdict:

```
Example A — Clearly Legitimate:
  URL: https://www.google.com
  → Legitimate Confidence:  97.3%
  → Phishing Confidence:     2.7%
  → Verdict: ✅ LEGITIMATE

Example B — Clear Phishing:
  URL: http://192.168.0.1/paypal-login/verify?user=admin
  → Legitimate Confidence:   4.1%
  → Phishing Confidence:    95.9%
  → Verdict: 🚨 PHISHING DETECTED

Example C — Ambiguous (treat with caution):
  URL: http://secure-bank-verify.co/login
  → Legitimate Confidence:  51.2%
  → Phishing Confidence:    48.8%
  → Verdict: ✅ LEGITIMATE (borderline — exercise caution)
```

> A score near 50% means the model is uncertain. Uncertainty itself is a useful signal — treat borderline URLs with extra care.

### 3. Risk Factor Breakdown — Why Did It Decide That?

Each prediction is explained through individual contributing signals, scored as risk-increasing (+) or risk-reducing (−):

| Signal | Score | Meaning |
|---|---|---|
| IP address used as domain | `+30` | Strong phishing indicator — real sites use domain names |
| URL obfuscation detected | `+25` | Encoded or disguised characters in URL |
| Password keyword in URL | `+20` | Likely a credential harvesting page |
| Banking keyword in URL | `+15` | Common lure tactic in phishing campaigns |
| Multiple subdomains | `+8` per level | Attackers nest fake subdomains to appear legitimate |
| Uses HTTPS | `−15` | Reduces risk, but HTTPS alone does not guarantee safety |
| Trusted TLD (`.com`, `.org`) | `−10` | Well-established domain extensions lower risk |
| Normal URL length | `−5` | Short URLs are less likely to hide malicious paths |

### 4. Visual Outputs in the App

Beyond the verdict and score, the Streamlit app renders four visual outputs:

**Confidence Gauge** — A semicircular dial showing the legitimate confidence score from 0% to 100%, colour-coded green (safe), amber (uncertain), or red (phishing).

**Safety Radar Chart** — A hexagonal radar showing 6 normalized safety dimensions:
- HTTPS usage, No IP domain, No obfuscation, Short URL, Trusted TLD, Low subdomain count

**Feature Bar Chart** — 10 key extracted features displayed as colour-coded horizontal bars. Red bars indicate risk-raising feature values; green bars indicate safe values.

**Risk Factor List** — All individual risk signals listed with their scores and a small progress bar visualizing their relative contribution to the final verdict.

### 5. Batch Scanner Output (CSV Download)

When scanning multiple URLs, the model produces a results table with one row per URL:

| Column | Description |
|---|---|
| `URL` | The input URL (truncated to 60 chars for display) |
| `Prediction` | ✅ Legitimate or 🚨 Phishing |
| `Legit %` | Probability the URL is legitimate |
| `Phish %` | Probability the URL is phishing |
| `HTTPS` | Whether the URL uses a secure connection |
| `URL Length` | Total character length of the URL |
| `Subdomains` | Number of subdomains detected |
| `Obfuscated` | Whether URL encoding / obfuscation was found |

This table can be downloaded as a `.csv` file for reporting or further analysis.

---

## 🚀 Live Demo

Run locally with one command (see [Quick Start](#-quick-start)):

```bash
streamlit run app.py
```

The app has three tabs:

- **🔍 URL Analyzer** — Paste any URL and get an instant prediction with confidence gauge, safety radar chart, and risk breakdown
- **📊 Model Insights** — Class distributions, model comparison charts, feature importance
- **📁 Batch Scanner** — Scan up to 100 URLs at once, download results as CSV

---

## 🗂️ Project Pipeline

```
Raw CSV Dataset (235,795 URLs)
        │
        ▼
┌─────────────────────┐
│  1. Data Loading    │  Shape: (235795, 56) · Target: label (0/1)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. EDA             │  Class balance · Correlations · Feature distributions
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Preprocessing   │  Drop text cols · Fill nulls · Train/Test split (80/20)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Feature Engg.   │  +5 derived features → 56 total input features
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  5. Model Training  │  6 classifiers · 5-fold Stratified CV
│  LR · DT · RF      │
│  GB · KNN · XGB     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  6. Evaluation      │  ROC-AUC · F1 · Confusion Matrix
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  7. Tuning          │  GridSearchCV on best model
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  8. Export          │  phishing_detector_model.pkl
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  9. Streamlit App   │  Real-time URL scanner · Batch mode · Insights
└─────────────────────┘
```

---

## 📦 Dataset

| Property | Value |
|---|---|
| **Name** | PhiUSIIL Phishing URL Dataset |
| **Source** | UCI Machine Learning Repository |
| **Total Records** | 235,795 URLs |
| **Features** | 56 (URL-based + page-level) |
| **Target** | `label` — `1` = Legitimate, `0` = Phishing |
| **Legitimate URLs** | 134,850 (57.2%) |
| **Phishing URLs** | 100,945 (42.8%) |

### Feature Categories

The dataset captures three types of signals:

**URL-based features** — Length, character counts, special symbols, TLD, subdomain count, obfuscation, HTTPS usage, digit/letter ratios

**Domain-level features** — IP address usage, TLD legitimacy probability, domain length, URL similarity index

**Page-level features** — HTTPS cert, favicon, robots.txt, external links, iFrames, popup count, social network links, copyright info, password/hidden fields

> **Note:** Page-level features (HTML content) default to `0` in the Streamlit app since it performs static URL analysis without fetching page content.

---

## 📊 Model Results

All models evaluated on a held-out **20% test set** (47,159 samples):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| 🥇 **Random Forest** | **0.9871** | **0.9880** | **0.9876** | **0.9872** | **0.9981** |
| 🥈 XGBoost | 0.9868 | 0.9875 | 0.9870 | 0.9869 | 0.9985 |
| 🥉 Gradient Boosting | 0.9742 | 0.9751 | 0.9748 | 0.9743 | 0.9963 |
| KNN | 0.9401 | 0.9415 | 0.9410 | 0.9403 | 0.9714 |
| Decision Tree | 0.9699 | 0.9704 | 0.9704 | 0.9701 | 0.9701 |
| Logistic Regression | 0.9211 | 0.9220 | 0.9215 | 0.9212 | 0.9804 |

**Winner: Random Forest** with F1 = **0.9872** and ROC-AUC = **0.9981** after hyperparameter tuning.

### Top Predictive Features

1. `URLSimilarityIndex` — How similar the URL is to known legitimate patterns
2. `TLDLegitimateProb` — Statistical legitimacy of the top-level domain
3. `CharContinuationRate` — Repeated character patterns (common in obfuscated URLs)
4. `URLCharProb` — Proportion of alphanumeric characters
5. `IsHTTPS` — Whether the URL uses a secure protocol

---

## 📁 Project Structure

```
day50-58/
│
├── 📓 phishing_url_detection.ipynb     # Full ML pipeline notebook
├── 🌐 app.py                           # Streamlit web application
├── 📋 README.md                        # This file
├── 📦 requirements.txt                 # Python dependencies
│
├── 📊 PhiUSIIL_Phishing_URL_Dataset.csv  # Dataset (place here before running)
│
└── 🤖 (generated after running notebook)
    ├── phishing_detector_model.pkl     # Trained Random Forest model
    └── phishing_detector_scaler.pkl    # Fitted StandardScaler
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Aaronrao989/60-days_Global-Coding-Challenge_AB-Talks.git
cd 60-days_Global-Coding-Challenge_AB-Talks/day50-58
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost streamlit joblib
```

### 4. Place the Dataset

Download the dataset and place it in the `day50-58/` folder:

```
day50-58/
└── PhiUSIIL_Phishing_URL_Dataset.csv   ← put it here
```

---

## 📓 Running the Notebook

The notebook walks through the entire ML pipeline from EDA to model export.

```bash
# Start Jupyter
jupyter notebook phishing_url_detection.ipynb

# Or use JupyterLab
jupyter lab phishing_url_detection.ipynb
```

**Run all cells top-to-bottom.** At the end, two files will be saved:

```
phishing_detector_model.pkl     ← trained model
phishing_detector_scaler.pkl    ← fitted scaler
```

> ⚠️ These `.pkl` files **must exist** before launching the Streamlit app for full model predictions. Without them, the app falls back to a heuristic rule-based scorer.

### Notebook Sections

| # | Section | Description |
|---|---|---|
| 1 | Setup | Library imports |
| 2 | Data Loading | Load CSV, shape, types |
| 3 | EDA | Distributions, correlations, class analysis |
| 4 | Preprocessing | Clean, split, scale |
| 5 | Feature Engineering | 5 new derived features |
| 6 | Model Comparison | 6 classifiers with 5-fold CV |
| 7 | Best Model Evaluation | Report, confusion matrix, ROC |
| 8 | Hyperparameter Tuning | GridSearchCV |
| 9 | Feature Importance | Top features + cumulative plot |
| 10 | Error Analysis | False negatives / positives |
| 11 | Summary | Final metrics + rankings |
| 12 | Export | Save model with joblib |

---

## 🌐 Running the Web App

Make sure you have run the notebook first to generate the `.pkl` files, then:

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

### App Features

#### Tab 1 — 🔍 URL Analyzer
- Paste any URL and click **Analyze →**
- Instant prediction: Legitimate ✅ or Phishing 🚨
- Confidence gauge (0–100%)
- Safety radar chart (6 key dimensions)
- Feature bar chart with color-coded risk levels
- Risk factor breakdown with individual scores
- Full feature table (expandable)

#### Tab 2 — 📊 Model Insights
- Dataset overview (class counts, feature count)
- Class distribution pie chart
- Model comparison bar chart (F1-Score)
- Feature importance chart (Top 15)
- Full metrics comparison table

#### Tab 3 — 📁 Batch Scanner
- Paste up to 100 URLs (one per line), OR upload a `.txt` / `.csv` file
- Scans all URLs with progress bar
- Summary cards: total scanned, legitimate count, phishing count
- Confidence score distribution histogram
- Full results table
- **Download results as CSV**

### Troubleshooting the App

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Model not found warning | Run the notebook first to generate `.pkl` files |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Slow on first run | Model loads into cache; subsequent predictions are fast |

---

## 🔧 Feature Engineering

Five new features were derived during preprocessing:

| Feature | Formula | Intuition |
|---|---|---|
| `DigitLetterRatio` | `digits / (letters + 1)` | Phishing URLs have more random digits |
| `TotalSpecialChars` | `= + ? + & + other special` | High special char count = more suspicious |
| `URLToDomainRatio` | `URLLength / (DomainLength + 1)` | Very long paths relative to domain = suspicious |
| `HasExternalResources` | `1 if external refs > 0` | Binary flag for external content |
| `HasRedirect` | `1 if redirects > 0` | Binary flag for URL redirects |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Pandas / NumPy** | Data manipulation |
| **Matplotlib / Seaborn** | EDA visualizations |
| **scikit-learn** | ML models, preprocessing, evaluation |
| **XGBoost** | Gradient boosted classifier |
| **Joblib** | Model serialization |
| **Streamlit** | Interactive web application |
| **Jupyter Notebook** | Development environment |

---

## 💡 Key Insights

- **HTTPS alone is not enough** — 23% of phishing URLs in this dataset use HTTPS
- **URL length is a strong signal** — phishing URLs average 94 chars vs 67 for legitimate
- **TLD matters** — phishing URLs heavily use `.xyz`, `.tk`, `.ml`, `.ga` with very low legitimacy scores
- **IP-based domains** are almost exclusively phishing (IsDomainIP = 1 → ~96% phishing)
- **Just 10 features** explain over 90% of the model's predictive power
- **False negatives are the key risk** — missed phishing URLs are more dangerous than false alarms

---

## 👤 Author

**Aaron Rao**  
60-Days Global Coding Challenge · AB Talks  
Days 50–58: Data Science Capstone

🔗 [GitHub Repository](https://github.com/Aaronrao989/60-days_Global-Coding-Challenge_AB-Talks)  
📁 [Day 50–58 Folder](https://github.com/Aaronrao989/60-days_Global-Coding-Challenge_AB-Talks/tree/main/day50-58)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ as part of the 60-Days Global Coding Challenge · AB Talks</sub>
</div>