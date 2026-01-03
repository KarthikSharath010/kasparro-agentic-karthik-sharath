import json
from agents.base import BaseAgent

class IdeationAgent(BaseAgent):
    def __init__(self, state):
        super().__init__("IdeationAgent", state)

    def execute(self):
        # 1. Brainstorm Questions
        if not self.state.get_context("raw_questions"):
            if self.state.get_context("simulation_mode"):
                self.state.log_event(self.name, "[Sim] Brainstorming questions...")
                questions = "1. How often should I use it?\n2. Is it safe for sensitive skin?\n3. Can I use it with Retinol?"
                self.state.update_context("raw_questions", questions)
            else:
                self.state.log_event(self.name, "Starting ideation phase...")
                prompt = "Generate 5 common customer questions about Vitamin C Serums. Return numbered list."
                response = self.call_llm(prompt)
                if response:
                    self.state.update_context("raw_questions", response)
                else:
                    return

        # 2. Structure/Categorize
        if not self.state.get_context("structured_faqs"):
            if self.state.get_context("simulation_mode"):
                self.state.log_event(self.name, "[Sim] Categorizing questions...")
                structured = {
                    "categories": [
                        {"name": "Usage", "questions": ["How often should I use it?", "Can I use it with Retinol?"]},
                        {"name": "Suitability", "questions": ["Is it safe for sensitive skin?"]}
                    ]
                }
                self.state.update_context("structured_faqs", structured)
            else:
                raw = self.state.get_context("raw_questions")
                prompt = f"Categorize these questions into Usage, Benefits, Suitability. JSON: {{ 'categories': [ {{ 'name': '...', 'questions': [...] }} ] }}\n{raw}"
                response_json = self.call_llm(prompt, json_mode=True)
                if response_json:
                    try:
                        data = json.loads(response_json)
                        self.state.update_context("structured_faqs", data)
                    except:
                        pass
