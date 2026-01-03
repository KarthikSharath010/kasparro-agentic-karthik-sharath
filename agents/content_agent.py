import json
from agents.base import BaseAgent

class ContentAgent(BaseAgent):
    def __init__(self, state):
        super().__init__("ContentAgent", state)

    def execute(self):
        self.state.log_event(self.name, "Starting content assembly...")
        
        sim_mode = self.state.get_context("simulation_mode")

        # 1. Build FAQ JSON
        if "faq.json" not in self.state.get_all()["artifacts"]:
            self.state.log_event(self.name, "Building FAQ JSON...")
            if sim_mode:
                faq_data = {
                    "faqs": [
                        {"question": "How often should I use it?", "answer": "For best results, apply GlowBoost Vitamin C Serum every morning after cleansing."},
                        {"question": "Is it safe for sensitive skin?", "answer": "Yes, GlowBoost is formulated with soothing ingredients like Vitamin E and is suitable for sensitive skin."},
                        {"question": "Can I use it with Retinol?", "answer": "We recommend using Vitamin C in the morning and Retinol at night to avoid irritation."}
                    ]
                }
                self.state.save_artifact("faq.json", faq_data)
            else:
                # Real Logic
                faqs = self.state.get_context("structured_faqs")
                glow_data = self.state.get_context("glowboost_data")
                prompt = f"Create FAQ JSON from {json.dumps(faqs)} using info {json.dumps(glow_data)}. JSON: {{ 'faqs': [ {{ 'question': '...', 'answer': '...' }} ] }}"
                content = self.call_llm(prompt, json_mode=True)
                if content:
                    self.state.save_artifact("faq.json", json.loads(content))

        # 2. Build Product Page JSON
        if "product_page.json" not in self.state.get_all()["artifacts"]:
            self.state.log_event(self.name, "Building Product Page JSON...")
            if sim_mode:
                pp_data = {
                    "meta": {"title": "GlowBoost | Radiance Defined", "description": "Experience the power of 20% Vitamin C."},
                    "hero_section": {
                        "headline": "Unlock Your Inner Radiance",
                        "subheadline": "Advanced Vitamin C therapy for brighter, smoother skin.",
                        "call_to_action": "Shop Now",
                        "key_benefits": ["Brightens Complexion", "Fades Dark Spots", "Daily Protection"]
                    },
                    "specifications": {
                        "volume": "30ml / 1.0 fl oz",
                        "price": 29.99,
                        "ingredients": ["Aqua", "Ascorbic Acid (20%)", "Tocopherol (Vitamin E)", "Ferulic Acid", "Hyaluronic Acid"]
                    }
                }
                self.state.save_artifact("product_page.json", pp_data)
            else:
                glow_data = self.state.get_context("glowboost_data")
                prompt = f"Create Product Page JSON for {json.dumps(glow_data)}. Structure: meta, hero_section, specifications."
                content = self.call_llm(prompt, json_mode=True)
                if content:
                    self.state.save_artifact("product_page.json", json.loads(content))

        # 3. Build Comparison JSON
        if "comparison_page.json" not in self.state.get_all()["artifacts"]:
            self.state.log_event(self.name, "Building Comparison JSON...")
            if sim_mode:
                comp_data = {
                    "comparison_points": [
                        {"feature": "Vitamin C Conc.", "glowboost": "20%", "competitor": "15%"},
                        {"feature": "Price", "glowboost": "$29.99", "competitor": "$45.00"},
                        {"feature": "Cruelty-Free", "glowboost": "Yes", "competitor": "No"}
                    ]
                }
                self.state.save_artifact("comparison_page.json", comp_data)
            else:
                glow_data = self.state.get_context("glowboost_data")
                comp = self.state.get_context("competitor_data")
                prompt = f"Compare GlowBoost vs {comp.get('name')}. JSON: {{ 'comparison_points': [...] }}"
                content = self.call_llm(prompt, json_mode=True)
                if content:
                    self.state.save_artifact("comparison_page.json", json.loads(content))
        
        self.state.log_event(self.name, "All artifacts assembled.")
