import json
import os
import google.generativeai as genai

class DataAgent:
    def __init__(self, source_path="library/glowboost.json"):
        self.source_path = source_path
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            self.model = None

    def load_glowboost_data(self):
        """Loads the authoritative GlowBoost dataset."""
        if not os.path.exists(self.source_path):
            return None
        with open(self.source_path, "r") as f:
            return json.load(f)

    def generate_competitor_data(self):
        """
        Generates 'Product B' for comparison using LLM.
        """
        # Fallback if no LLM
        fallback = {
            "product_name": "RadianceRetinol Night Serum (Fallback)",
            "category": "Skincare",
            "price": 45.00,
            "size": "30ml",
            "ingredients": ["Retinol", "Vitamin E", "Aqua"],
            "claims": ["Anti-aging"]
        }
        
        if not self.model:
            return fallback

        prompt = """
        Generate a fictional competitor skincare product JSON to compare against a Vitamin C Serum.
        It should be a "Retinol" product.
        Format:
        {
            "product_name": "Str",
            "category": "Skincare",
            "price": Float,
            "size": "30ml",
            "ingredients": ["List", "Of", "5", "Ingredients"],
            "claims": ["List", "Of", "3", "Claims"]
        }
        Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple cleaning to ensure JSON parsing
            clean_text = response.text.strip().lstrip("```json").rstrip("```")
            return json.loads(clean_text)
        except:
            return fallback
