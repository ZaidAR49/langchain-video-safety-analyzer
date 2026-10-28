# Video Brand Safety & Compliance Analyzer — Specification

> **System:** Brand Safety & Content Compliance Engine  
> **Framework:** LangChain & Google Gemini  
> **Package Management:** `uv`  

---

## 🎯 1. System Overview & Objective

An automated brand-safety auditor for content creators, marketing agencies, and brand sponsorship managers.

Before publishing sponsored video content or partnering with creators, media managers input a **video URL** and select sensitive categories to inspect:
- 🍺 Alcohol & Drinking
- 🚬 Smoking / Drugs
- 🎲 Gambling & Betting
- 🤬 Profanity & Hate Speech
- 🔞 Adult / Sensitive Content
- ⚔️ Violence & Dangerous Activities

The engine analyzes the video content and generates a **structured compliance report** containing:
1. **Overall Verdict:** `SAFE` ✅, `CAUTION` ⚠️, or `FLAGGED` 🚫
2. **Brand Safety Score:** `0% – 100%`
3. **Timestamped Incident Log:** Exact timestamp where each violation occurred.
4. **Actionable Recommendations:** Specific timestamps and instructions for video editing and policy compliance.

---

## 🏗️ 2. Technical Architecture

The system leverages:

1. **Multimodal Reasoning**:
   - Ingests public video streams directly via Gemini's multimodal video understanding engine.
2. **Schema Enforcement & Structured Output**:
   - Pydantic models (`ViolationItem`, `SafetyReport`) enforce deterministic JSON output schemas.
3. **Execution Pipeline**:
   - Orchestrates system prompt instructions, multimodal input payloads, and the model via LangChain.

---

## 📦 3. Dependencies

Managed via `uv`:

```bash
uv add langchain langchain-google-genai pydantic python-dotenv streamlit
```

---

## 📁 4. Project Layout

```
langchain/
├── .env                       # GEMINI_API_KEY
├── .env.example               # Template showing required environment variables
├── pyproject.toml             # uv project configuration
├── PROJECT_BRIEF.md           # Product and technical specifications
├── README.md                  # Project overview and run guide
└── src/
    └── video_safety/
        ├── __init__.py        # Package entrypoint
        ├── schemas.py         # Pydantic schemas (ViolationItem, SafetyReport)
        ├── analyzer.py        # Core multimodal inspection pipeline
        ├── app.py             # Streamlit Web UI
        └── main.py            # Unified entrypoint (Web UI & CLI)
```

---

## 🚀 5. Execution Modes

The application supports dual operation modes:

1. **Interactive Web Dashboard (Streamlit)**:
   - Run: `uv run python -m video_safety.main`
   - Features video preview, category configuration, safety score gauge, and incident tables.

2. **Automated Command-Line Interface (CLI)**:
   - Run: `uv run python -m video_safety.main --cli [URL]`
   - Formats and outputs the compliance verdict, incident log, and recommendations to the console.
