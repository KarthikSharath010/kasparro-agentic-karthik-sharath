import json
from agents.base import BaseAgent

class DataAgent(BaseAgent):
    def __init__(self, state):
        super().__init__("DataAgent", state)

    def execute(self):
        # 1. Load Source Data
        if not self.state.get_context("glowboost_data"):
            self.state.log_event(self.name, "Starting data ingestion...")
            glowboost_data = {
                "product_name": "GlowBoost Vitamin C Serum",
                "ingredients": ["Vitamin C (20%)", "Vitamin E", "Hyaluronic Acid", "Ferulic Acid"],
                "benefits": ["Brightens skin", "Reduces fine lines", "Hydrates", "Protects against UV"],
                "price": 29.99
            }
            self.state.update_context("glowboost_data", glowboost_data)
            self.state.log_event(self.name, "Loaded GlowBoost data successfully.")
        
        # 2. Generate Competitor Data
        if not self.state.get_context("competitor_data"):
            if self.state.get_context("simulation_mode"):
                self.state.log_event(self.name, "[Sim] Generating competitor data...")
                competitor_name = "LuminaEssence Brightening Drops"
                self.state.update_context("competitor_data", {"name": competitor_name})
                self.state.log_event(self.name, f"Generated Competitor: {competitor_name}")
            else:
                # Real LLM Call
                self.state.log_event(self.name, "Generating competitor data...")
                prompt = "Generate a fictional competitor product to 'GlowBoost Vitamin C Serum'. Return ONLY the name."
                competitor_name = self.call_llm(prompt)
                if competitor_name:
                    self.state.update_context("competitor_data", {"name": competitor_name.strip()})
                    self.state.log_event(self.name, f"Generated Competitor: {competitor_name.strip()}")
                else:
                    self.state.log_event(self.name, "Failed to generate competitor.")
