import json
from agents.base import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self, state):
        super().__init__("ValidatorAgent", state)

    def execute(self):
        if self.state.get_context("simulation_mode"):
            self.state.log_event(self.name, "[Sim] Validating artifacts...")
            # Simulate a "Pass"
            self.state.update_context("validation_report", "PASS")
            self.state.log_event(self.name, "Validation Successful (Simulation).")
            return

        # Real Logic
        self.state.log_event(self.name, "Validating artifacts...")
        artifacts = self.state.get_all()["artifacts"]
        
        prompt = f"""
        Audit these artifacts:
        1. FAQ: {json.dumps(artifacts.get('faq.json', {}))}
        2. Product: {json.dumps(artifacts.get('product_page.json', {}))}
        
        Rules:
        - FAQ must have at least 3 items.
        - Product Page must have 'price'.
        
        Return JSON: {{ "status": "PASS" or "FAIL", "critique": "..." }}
        """
        
        response = self.call_llm(prompt, json_mode=True)
        if response:
            try:
                data = json.loads(response)
                status = data.get("status", "FAIL")
                self.state.update_context("validation_report", status)
                self.state.log_event(self.name, f"Validation {status}: {data.get('critique', 'No critique')}")
            except:
                self.state.update_context("validation_report", "FAIL")
