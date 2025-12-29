# 🤖 ApexAgent: Modular Content Generation Pipeline
### **Autonomous Multi-Agent System for Structured Market Intelligence**

ApexAgent is a production-grade agentic automation system designed to transform raw, unstructured product data into high-fidelity, machine-readable marketing assets. Built for the Kasparro Applied AI Engineering Challenge, it demonstrates the power of modular agent orchestration over monolithic prompting.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange?logo=google-gemini)

---

## 🏗️ System Architecture

The project follows a **Directed Acyclic Graph (DAG)** orchestration, ensuring clear boundaries and deterministic data flow between specialized agents.

### **The Multi-Agent Graph**
1.  **Data Ingestion Agent**: Parses the "GlowBoost" source-of-truth and autonomously models a fictional competitor (e.g., *RadianceRetinol*) to facilitate comparative analysis.
2.  **Ideation Agent**: Generates 20+ categorized consumer questions (Safety, Usage, Science) strictly bounded by the input dataset to prevent hallucinations.
3.  **Content Assembly Agent**: The master orchestrator that triggers **Deterministic Logic Blocks** and maps processed data into validated JSON templates.

---

## 🛠️ Key Engineering Features

* **Deterministic Logic Blocks**: Moves beyond "creative writing" by implementing standalone Python functions for price delta calculations and ingredient overlap analysis.
* **Zero-Hallucination Policy**: Every agent operates under a strict "Source-Only" context constraint, ensuring 100% factual alignment with the `glowboost.json` dataset.
* **Template-First Design**: Utilizes a custom template engine to ensure all outputs strictly adhere to pre-defined JSON schemas, making them instantly machine-readable.
* **System Observability**: Integrated "System Health" monitor in the UI tracks real-time **API Latency**, **Token Consumption**, and **Processing Costs**.

---

## 📂 Project Structure

```text
├── app.py                # Main Pipeline Orchestrator & UI
├── agents/
│   ├── data_agent.py     # Source Ingestion & Competitor Modeling
│   ├── ideation_agent.py # Categorized FAQ Generation
│   └── content_agent.py  # Final JSON Assembly & Validation
├── core/
│   ├── logic_blocks.py   # Deterministic Math & Comparison Logic
│   └── templates.py      # JSON Schemas (FAQ, Product, Comparison)
├── library/
│   └── glowboost.json    # The "Source of Truth" Input Dataset
└── docs/
    └── projectdocumentation.md # Technical Design & Flowcharts

```

---

## 🚀 Installation & Setup

1. **Clone the Repository**:
```bash
git clone [https://github.com/KarthikSharath010/kasparro-ai-agentic-content-generation-system-karthik-sharath.git](https://github.com/KarthikSharath010/kasparro-ai-agentic-content-generation-system-karthik-sharath.git)
cd kasparro-ai-agentic-content-generation-system-karthik-sharath

```


2. **Install Dependencies**:
```bash
pip install -r requirements.txt

```


3. **Configure API Access**:
Add your `GOOGLE_API_KEY` to a `.env` file or enter it directly into the Streamlit sidebar.
4. **Run the Pipeline**:
```bash
streamlit run app.py

```



---

## 📊 Evaluation Criteria Alignment

* **Modularity (45%)**: Each agent has a single responsibility and no shared global state.
* **Agent Quality (25%)**: Meaningful roles with strict input/output boundaries.
* **Content Engineering (20%)**: Reusable logic blocks and a robust template engine.
* **Data Integrity (10%)**: Validated JSON artifacts (FAQ, Product Page, Comparison).

---

**Developed for the Kasparro Applied AI Engineering Submission.**

