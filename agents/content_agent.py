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
