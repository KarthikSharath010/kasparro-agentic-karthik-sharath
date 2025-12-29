# kasparro-ai-agentic-content-generation-system-karthik-sharath

> **ApexAgent**: A Multi-Agent AI System transforming raw product data into structured market assets.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/AI-Gemini%20Flash-orange)

## 🚀 Overview

This project implements a modular content generation pipeline that ingests raw product data (JSON), enriches it using LLMs (Google Gemini), and outputs structured artifacts for e-commerce, including:
- **Product Landing Page** (`product_page.json`)
- **FAQ Database** (`faq.json`)
- **Competitor Comparison** (`comparison_page.json`)

## 🏗️ Architecture

The system follows a sequential multi-agent design:
1.  **Data Agent**: Loads the source of truth (`glowboost.json`) and generates synthetic competitor models.
2.  **Ideation Agent**: Uses Generative AI to brainstorm customer-centric questions.
3.  **Content Agent**: Deterministically formats logic and calculates insights (e.g., Price/ml).

## 🛠️ Setup & Run

### 1. Clone & Install
```bash
git clone https://github.com/your-username/kasparro-pipeline.git
cd kasparro-pipeline
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_key_here
```
*Alternatively, enter the key in the sidebar UI.*

### 3. Launch App
```bash
streamlit run app.py
```

## 🧠 Features
- **Visual Orchestration**: Live stepper UI to track agent progress.
- **Engineered Insights**: Logic blocks proving deterministic math over LLM hallucination.
- **Standout UI**: Premium glassmorphism aesthetics and responsive layout.

---
*Built for the Kasparro Assignment.*
