import google.generativeai as genai
import os
from core.logic_blocks import categorize_question

class IdeationAgent:
    def __init__(self):
        self.model = None
        self.init_error = None
        # Assumes GEMINI_API_KEY is found in environment or previously set
        try:
            self.model = genai.GenerativeModel('gemini-flash-latest')
        except Exception as e:
            self.init_error = str(e)
            self.model = None

    def generate_questions(self, product_data):
        """Generates 15+ candidate questions based on product data."""
        if not self.model:
            error_msg = f"Error: Gemini API key not configured/invalid. Details: {self.init_error}"
            return [error_msg]
        
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
