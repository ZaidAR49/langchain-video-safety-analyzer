# 🛡️ Video Brand Safety & Compliance Analyzer

An automated brand-safety auditor for content creators, marketing agencies, and brand sponsorship managers.

The system evaluates video streams (such as public YouTube URLs) against advertising compliance guidelines and sensitive brand-safety categories, returning a structured audit report with timestamped violation logs and editing recommendations.

---

## 🎯 Key Capabilities

* **Automated Video Compliance Auditing**: Evaluates public video content directly via multimodal reasoning without manual frame extraction.
* **Granular Policy Detection**: Detects violations across sensitive categories:
  * 🍺 **Alcohol & Drinking**
  * 🚬 **Smoking & Substance Use**
  * 🎲 **Gambling & Betting**
  * 🤬 **Profanity & Hate Speech**
  * 🔞 **Adult / Inappropriate Content**
  * ⚔️ **Violence & Dangerous Stunts**
* **Deterministic Structured Output**: Powered by Pydantic models to guarantee typed JSON responses with overall verdict (`SAFE`, `CAUTION`, `FLAGGED`), safety score (`0-100`), incident timestamps, and remediation recommendations.
* **Dual Interface & Bilingual Support**: Includes an interactive bilingual Streamlit Web UI (English & Arabic with native RTL layout) and a scriptable CLI.

---

## 🏗️ Architecture & Technology Stack

* **Orchestration**: LangChain (`ChatGoogleGenerativeAI`, messages, LCEL)
* **Model**: Google Gemini (`gemini-3.5-flash-lite` with native multimodal video understanding)
* **Data Validation**: Pydantic v2
* **Web Interface**: Streamlit
* **Package Management**: `uv`

---

## 📁 Project Structure

```
langchain/
├── .env                       # Environment variables (GEMINI_API_KEY)
├── .env.example               # Reference template for configuration
├── pyproject.toml             # uv configuration and dependencies
├── README.md                  # Project documentation
├── PROJECT_BRIEF.md           # Product specification and requirements
└── src/
    └── video_safety/
        ├── __init__.py        # Package initialization
        ├── schemas.py         # Pydantic data schemas (ViolationItem, SafetyReport)
        ├── analyzer.py        # LangChain & Gemini multimodal analysis pipeline
        ├── app.py             # Streamlit Web UI
        └── main.py            # Entry point dispatcher (Web UI or CLI)
```

---

## ⚙️ Quickstart & Installation

### Prerequisites
* Python 3.11+
* [`uv`](https://docs.astral.sh/uv/) package manager
* Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Configure Environment
Create a `.env` file from `.env.example`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies
```bash
uv sync
```

---

## 🚀 Running the Application

### Option A: Streamlit Web UI (Default)
```bash
uv run python -m video_safety.main
```
Or run directly via Streamlit:
```bash
uv run streamlit run src/video_safety/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### Option B: Command-Line Interface (CLI)
```bash
# Run with sample video:
uv run python -m video_safety.main --cli

# Run with custom video URL:
uv run python -m video_safety.main --cli "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
```
