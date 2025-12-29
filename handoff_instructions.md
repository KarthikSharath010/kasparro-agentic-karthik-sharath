# 📦 Kasparro Project Handoff Protocol

**System Context:**
We are building a "Content Generation Pipeline" for the Kasparro assignment. The system takes a specific input (`glowboost.json`) and uses a Multi-Agent architecture to generate three specific JSON artifacts (`product_page.json`, `faq.json`, `comparison_page.json`).

**Goal:**
Complete the content generation pipeline. The code is structured, functional, and adhering to strict logic separation (Agents vs. Core Logic).

**Current Status:**
- [x] **Architecture**: Split into `DataAgent`, `IdeationAgent`, and `ContentAgent`.
- [x] **Logic**: Templates and Logic Blocks are implemented in `core/`.
- [x] **UI**: A Streamlit app (`app.py`) orchestrates the flow.
- [ ] **Verification**: Needs robust testing of the generated JSONs.
- [ ] **Refinement**: Improve the "Ideation" prompts for better quality questions.

---

## 📂 File System Reconstruction

Please recreate the following file structure and contents exactly.

### 1. `requirements.txt`
*Dependencies required to run the system.*
```text
streamlit
google-generativeai
python-dotenv
```

### 2. `library/glowboost.json`
*The single source of truth for input data.*
```json
{
  "product_name": "GlowBoost Vitamin C Serum",
  "category": "Skincare",
  "price": 29.99,
  "size": "30ml",
  "target_audience": ["Dull Skin", "Anti-Aging", "Hyperpigmentation"],
  "ingredients": [
    "Vitamin C (20% L-Ascorbic Acid)",
    "Vitamin E",
    "Hyaluronic Acid",
    "Ferulic Acid",
    "Glycerin",
    "Aqua"
  ],
  "claims": [
    "Brightens skin tone in 7 days",
    "Reduces appearance of fine lines",
    "Hydrates and plumps skin",
    "Cruelty-free and Vegan"
  ],
  "usage_instructions": "Apply 3-4 drops to clean, dry face every morning. Follow with moisturizer and sunscreen.",
  "safety_warnings": "Patch test before use. Discontinue if irritation occurs. Keep out of sunlight.",
  "faqs_raw": [
    {
      "q": "Can I use this with Retinol?",
      "a": "It is best to use Vitamin C in the morning and Retinol at night to avoid irritation."
    },
    {
      "q": "Is it suitable for sensitive skin?",
      "a": "Yes, but we recommend a patch test due to the potency of Vitamin C."
    },
    {
      "q": "Does it oxidize?",
      "a": "Our formula uses stabilized L-Ascorbic acid and dark glass packaging to minimize oxidation."
    }
  ]
}
```

### 3. `core/templates.py`
*Enforces strict JSON output schemas.*
```python
"""
Template Engine for Kasparro Content Generation.
Defines the required structure for final JSON outputs.
"""

def get_faq_template():
    return {
        "generated_at": "",
        "categories": {
            "Usage": [],
            "Safety": [],
            "Science": [],
            "General": []
        },
        "total_questions": 0
    }

def get_product_page_template():
    return {
        "meta": {
            "title": "",
            "description": ""
        },
        "hero_section": {
            "headline": "",
            "key_benefits": []
        },
        "specifications": {
            "price": 0.0,
            "volume": "",
            "ingredients": []
        },
        "usage_guide": "",
        "call_to_action": ""
    }

def get_comparison_page_template():
    return {
        "products": {
            "product_a": "",
            "product_b": ""
        },
        "comparison_points": [
            # { "feature": "", "product_a_val": "", "product_b_val": "", "winner": "" }
        ],
        "summary": ""
    }
```

### 4. `core/logic_blocks.py`
*Pure functions for repeatable logic steps.*
```python
"""
Logic Blocks for Content Generation.
Reusable, modular functions for data processing.
"""

def calculate_price_per_ml(price, volume_str):
    """Calculates price per ml given a price and a string like '30ml'."""
    try:
        vol = float(volume_str.lower().replace("ml", "").strip())
        if vol == 0: return 0
        return round(price / vol, 2)
    except:
        return 0

def find_common_ingredients(list_a, list_b):
    """Returns list of ingredients found in both products."""
    set_a = {i.lower() for i in list_a}
    set_b = {i.lower() for i in list_b}
    return list(set_a.intersection(set_b))

def format_price_comparison(price_a, price_b, name_a, name_b):
    """Returns a structured comparison string for pricing."""
    diff = abs(price_a - price_b)
    cheaper = name_a if price_a < price_b else name_b
    return f"{cheaper} is cheaper by ${diff:.2f}"

def categorize_question(question_text):
    """Simple keyword-based categorizer for questions."""
    q_lower = question_text.lower()
    if any(x in q_lower for x in ["safe", "irritation", "skin type", "reaction"]):
        return "Safety"
    if any(x in q_lower for x in ["use", "apply", "morning", "night", "routine"]):
        return "Usage"
    if any(x in q_lower for x in ["acid", "percent", "formula", "oxidize"]):
        return "Science"
    return "General"
```

### 5. `agents/data_agent.py`
*Handles data ingestion and competitor modeling.*
```python
import json
import os

class DataAgent:
    def __init__(self, source_path="library/glowboost.json"):
        self.source_path = source_path

    def load_glowboost_data(self):
        """Loads the authoritative GlowBoost dataset."""
        if not os.path.exists(self.source_path):
            return None
        with open(self.source_path, "r") as f:
            return json.load(f)

    def generate_competitor_data(self):
        """
        Generates 'Product B' (RadianceRetinol) for comparison.
        This fulfills the requirement to compare against another product.
        """
        return {
            "product_name": "RadianceRetinol Night Serum",
            "category": "Skincare",
            "price": 45.00,
            "size": "30ml",
            "ingredients": [
                "Retinol (0.5%)",
                "Vitamin E",
                "Glycerin",
                "Squalane",
                "Aqua"
            ],
            "claims": [
                "Anti-aging power",
                "Reduces deep wrinkles",
                "Night-time repair"
            ]
        }
```

### 6. `agents/ideation_agent.py`
*Handles creative tasks and LLM interaction.*
```python
import google.generativeai as genai
import os
from core.logic_blocks import categorize_question

class IdeationAgent:
    def __init__(self):
        # Assumes GEMINI_API_KEY is found in environment or previously set
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except:
            self.model = None

    def generate_questions(self, product_data):
        """Generates 15+ candidate questions based on product data."""
        if not self.model:
            return ["Error: Gemini API key not configured."]
        
        context = f"""
        Product: {product_data['product_name']}
        Category: {product_data['category']}
        Usage: {product_data.get('usage_instructions', '')}
        Safety: {product_data.get('safety_warnings', '')}
        
        Generate 20 distinct customer questions people might ask about this product.
        Return ONLY the questions, one per line.
        """
        
        try:
            response = self.model.generate_content(context)
            questions = [q.strip("- ").strip() for q in response.text.split("\n") if q.strip()]
            return questions
        except Exception as e:
            return [f"Error generating questions: {e}"]

    def process_faqs(self, raw_questions):
        """Categorizes raw questions into the structured format."""
        categorized = {
            "Usage": [],
            "Safety": [],
            "Science": [],
            "General": []
        }
        
        for q in raw_questions:
            cat = categorize_question(q)
            categorized[cat].append(q)
            
        return categorized
```

### 7. `agents/content_agent.py`
*Assembles the final artifacts.*
```python
import datetime
from core.templates import get_faq_template, get_product_page_template, get_comparison_page_template
from core.logic_blocks import calculate_price_per_ml, find_common_ingredients, format_price_comparison

class ContentAgent:
    def build_faq_json(self, categorized_questions, answers_map=None):
        """Assembles the faq.json."""
        template = get_faq_template()
        template["generated_at"] = datetime.datetime.now().isoformat()
        
        # In a real system, we'd generate answers too. 
        # For now, we structure the identified questions.
        for cat, questions in categorized_questions.items():
            for q in questions:
                entry = {"question": q, "answer": "Generated answer placeholder."}
                template["categories"][cat].append(entry)
                template["total_questions"] += 1
                
        return template

    def build_product_page_json(self, data):
        """Assembles the product_page.json."""
        template = get_product_page_template()
        
        template["meta"]["title"] = f"{data['product_name']} - Official Store"
        template["meta"]["description"] = f"Buy {data['product_name']}. {data['claims'][0]}."
        
        template["hero_section"]["headline"] = f"Experience {data['claims'][0]}"
        template["hero_section"]["key_benefits"] = data['claims']
        
        template["specifications"]["price"] = data['price']
        template["specifications"]["volume"] = data['size']
        template["specifications"]["ingredients"] = data['ingredients']
        
        template["usage_guide"] = data.get("usage_instructions", "")
        template["call_to_action"] = "Add to Cart"
        
        return template

    def build_comparison_page_json(self, product_a, product_b):
        """Assembles the comparison_page.json logic."""
        template = get_comparison_page_template()
        
        template["products"]["product_a"] = product_a['product_name']
        template["products"]["product_b"] = product_b['product_name']
        
        # 1. Price Comparison
        price_a_ml = calculate_price_per_ml(product_a['price'], product_a['size'])
        price_b_ml = calculate_price_per_ml(product_b['price'], product_b['size'])
        
        template["comparison_points"].append({
            "feature": "Price per ml",
            "product_a_val": f"${price_a_ml}/ml",
            "product_b_val": f"${price_b_ml}/ml",
            "winner": product_a['product_name'] if price_a_ml < price_b_ml else product_b['product_name']
        })
        
        # 2. Ingredient Overlap
        common = find_common_ingredients(product_a['ingredients'], product_b['ingredients'])
        template["comparison_points"].append({
            "feature": "Common Ingredients",
            "product_a_val": str(len(common)),
            "product_b_val": str(len(common)),
            "note": f"Both contain: {', '.join(common)}"
        })
        
        template["summary"] = f"While {product_b['product_name']} is a strong competitor, {product_a['product_name']} offers better value at ${price_a_ml}/ml."
        
        return template
```

### 8. `app.py`
*The main entry point and UI.*
```python
import streamlit as st
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our new Agents
from agents.data_agent import DataAgent
from agents.ideation_agent import IdeationAgent
from agents.content_agent import ContentAgent

# --- Configuration ---
st.set_page_config(
    page_title="Kasparro Content Gen | GlowBoost",
    page_icon="✨",
    layout="wide",
)

# --- Sidebar ---
with st.sidebar:
    st.title("✨ Kasparro System")
    st.caption("Agentic Content Generation")
    st.info("Target: GlowBoost Vitamin C Serum")
    
    api_key = st.text_input("Gemini API Key (Optional if in .env)", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        import google.generativeai as genai
        genai.configure(api_key=api_key)

# --- Main Page ---
st.title("Agentic Content Generation Pipeline")
st.markdown("""
This system uses a **Multi-Agent Architecture** to transform raw data into structured content:
1.  **Data Agent**: Ingests Source JSON & Models Competitor.
2.  **Ideation Agent**: Generates & Categorizes FAQs.
3.  **Content Agent**: Assembles final `product_page.json` and `comparison_page.json`.
""")

if st.button("🚀 Run Pipeline", type="primary"):
    with st.status("Executing Multi-Agent Workflow...", expanded=True) as status:
        
        # 1. Data Agent
        st.write("📦 **Data Agent**: Loading GlowBoost & Modeling Competitor...")
        data_agent = DataAgent()
        glowboost = data_agent.load_glowboost_data()
        competitor = data_agent.generate_competitor_data()
        
        if not glowboost:
            status.update(label="Error: Source data not found!", state="error")
            st.stop()
            
        st.json({"Source": glowboost['product_name'], "Competitor": competitor['product_name']}, expanded=False)
        
        # 2. Ideation Agent
        st.write("💡 **Ideation Agent**: Brainstorming Questions...")
        ideation_agent = IdeationAgent()
        raw_questions = ideation_agent.generate_questions(glowboost)
        structured_faqs = ideation_agent.process_faqs(raw_questions)
        st.markdown(f"Generated **{len(raw_questions)}** questions across {len(structured_faqs)} categories.")

        # 3. Content Agent
        st.write("📝 **Content Agent**: Assembling Final JSON Artifacts...")
        content_agent = ContentAgent()
        
        # Build Artifacts
        faq_json = content_agent.build_faq_json(structured_faqs)
        product_json = content_agent.build_product_page_json(glowboost)
        comparison_json = content_agent.build_comparison_page_json(glowboost, competitor)
        
        status.update(label="Pipeline Complete!", state="complete")

    # --- Results Display ---
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📄 Product Page")
        st.json(product_json, expanded=False)
        st.download_button(
            "Download product_page.json",
            data=json.dumps(product_json, indent=2),
            file_name="product_page.json",
            mime="application/json"
        )
        
    with col2:
        st.subheader("❓ FAQ Data")
        st.json(faq_json, expanded=False)
        st.download_button(
            "Download faq.json",
            data=json.dumps(faq_json, indent=2),
            file_name="faq.json",
            mime="application/json"
        )

    with col3:
        st.subheader("⚖️ Comparison")
        st.json(comparison_json, expanded=False)
        st.download_button(
            "Download comparison.json",
            data=json.dumps(comparison_json, indent=2),
            file_name="comparison_page.json",
            mime="application/json"
        )
```

## 🚀 Execution Instructions

1.  **Install dependencies**:
    `pip install streamlit google-generativeai python-dotenv`
2.  **Environment Variables**:
    Create a `.env` file with your `GEMINI_API_KEY`.
3.  **Run the App**:
    `streamlit run app.py`

## 🔮 Future Roadmap (Next Steps)
1.  **Verification**: Manually verify the JSON output structure against the assignment requirements (ensure checking for `price_per_ml` calculation accuracy).
2.  **Refinement**: Enhance the logic in `IdeationAgent` to filter out irrelevant questions.
3.  **Packaging**: Zip the solution for submission if required.
