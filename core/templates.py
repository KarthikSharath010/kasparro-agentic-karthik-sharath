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
