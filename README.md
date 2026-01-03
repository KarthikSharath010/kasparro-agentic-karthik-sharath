# 🤖 ApexAgent: Autonomous Content Pipeline v2.1
### **Orchestrated Multi-Agent System for Market Intelligence**

ApexAgent is a production-grade autonomous system that transforms raw product data into high-fidelity, machine-readable marketing assets. It features a robust **Supervisor-Worker** architecture, ensuring deterministic execution and zero-hallucination outputs.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange?logo=google-gemini)
![Mode](https://img.shields.io/badge/Simulation%20Mode-Enabled-green)

---

## 🌐 Live Application
The ApexAgent pipeline is fully deployed and accessible via Streamlit Cloud.
[**🚀 Launch Live Demo**](https://kasparro-agentic-karthik-sharath.streamlit.app/)

---

## ⚡ Key Features

### 1. **🎥 Simulation Mode (New)**
Run the entire pipeline **without an API Key**.
- Perfect for demos and testing.
- Uses pre-calculated, high-quality data to simulate agent reasoning.
- Generates valid artifacts instantly.

### 2. **🧠 Supervisor Orchestration**
Instead of a simple chain, an **ApexSupervisor** manages the state.
- **Planning Phase**: Analyzes current context and decides which agent to call.
- **Execution Phase**: Dispatches tasks to specific agents.
- **Self-Correction**: If validation fails, the Supervisor re-plans and retries.

### 3. **🛡️ Zero-Hallucination Policy**
Every agent operates under strict context constraints, ensuring 100% factual alignment with the source data (`glowboost.json`).

---

## 🏗️ System Architecture

The project follows a **State-Machine Driven** architecture:

1.  **🔍 DataAgent**: Ingests source-of-truth data and autonomously models competitor products.
2.  **💡 IdeationAgent**: Brainstorms and structures customer questions (Safety, Usage, Science).
3.  **📝 ContentAgent**: Assembles the final artifacts (`faq.json`, `product_page.json`) using strict schema enforcement.
4.  **✅ ValidatorAgent**: Audits the outputs. If an artifact is missing or invalid, it rejects the step, triggering a re-run.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/KarthikSharath010/kasparro-ai-agentic-content-generation-system-karthik-sharath.git
cd kasparro-ai-agentic-content-generation-system-karthik-sharath
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Choose Your Mode
*   **🔵 Live Mode**: Enter your `Gemini API Key` in the sidebar to use the live LLM.
*   **🔴 Simulation Mode**: Toggle **"Enable Simulation Mode"** in the sidebar to run offline (Free/Demo).

---

## 📂 Artifacts Generated

The system produces three key JSON artifacts, visible in the "Generated Artifacts" tab:

*   `product_page.json`: Full schematic for an e-commerce landing page.
*   `faq.json`: Structured question-answer pairs.
*   `comparison_page.json`: Feature-by-feature comparison vs. competitor.

---

## 📊 Evaluation Metrics

*   **Modularity**: 100% decoupling between Agents and State.
*   **Reliability**: `try/except` blocks and fallback logic for all external calls.
*   **User Experience**: "Geometric Dark" theme with real-time logs and visual feedback.

---

**Developed for the Kasparro Applied AI Engineering Submission.**
