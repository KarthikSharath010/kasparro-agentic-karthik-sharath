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
