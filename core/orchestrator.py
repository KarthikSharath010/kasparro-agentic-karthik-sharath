import json
import os
import google.generativeai as genai
from core.state import SharedState

class ApexSupervisor:
    def __init__(self, state: SharedState):
        self.state = state
        self.agents = {}
        self.max_steps = 15
        
        # Initialize Phase in State
        if not self.state.get_context("supervisor_phase"):
            self.state.update_context("supervisor_phase", "PLANNING")
        
        # Initialize Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def register_agent(self, name, agent_instance):
        self.agents[name] = agent_instance

    def determine_next_step(self):
        # --- SIMULATION MODE LOGIC ---
        if self.state.get_context("simulation_mode"):
            if not self.state.get_context("glowboost_data") or not self.state.get_context("competitor_data"):
                return {"next_action": "DataAgent", "reason": "[Sim] Ingesting data..."}
            if not self.state.get_context("structured_faqs"):
                return {"next_action": "IdeationAgent", "reason": "[Sim] Generating FAQs..."}
            artifacts = self.state.get_all()["artifacts"]
            if "faq.json" not in artifacts or "product_page.json" not in artifacts:
                return {"next_action": "ContentAgent", "reason": "[Sim] Constructing artifacts..."}
            if not self.state.get_context("validation_report"):
                return {"next_action": "ValidatorAgent", "reason": "[Sim] Validating outputs..."}
            return {"next_action": "FINISH", "reason": "[Sim] Mission Complete."}

        # --- GEMINI LOGIC ---
        if not self.model:
            return {"next_action": "ERROR", "reason": "No API Key"}

        context_keys = list(self.state._state["context"].keys())
        artifact_keys = list(self.state._state["artifacts"].keys())
        last_log = self.state._state["messages"][-3:] if self.state._state["messages"] else "None"

        prompt = f"""
        You are a Supervisor. Respond in JSON.
        Goal: Ensure 'faq.json', 'product_page.json', 'comparison_page.json' are created and validated.
        
        State:
        - Context: {context_keys}
        - Artifacts: {artifact_keys}
        - Recent Logs: {last_log}
        
        Logic:
        1. Missing 'glowboost_data' -> DataAgent.
        2. Missing 'structured_faqs' -> IdeationAgent.
        3. Missing artifacts -> ContentAgent.
        4. Unvalidated -> ValidatorAgent.
        5. All Done -> FINISH.
        
        Return JSON: {{ "next_action": "AGENT_NAME" or "FINISH", "reason": "..." }}
        """

        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                self.state.log_event("Supervisor", "🛑 Quota Limit Hit. Wait 60s.")
            self.state.log_event("Supervisor", f"Planning Error: {error_msg}")
            return {"next_action": "FINISH", "reason": "Error during planning"}

    def run_step(self):
        phase = self.state.get_context("supervisor_phase")
        
        if phase == "PLANNING":
            plan = self.determine_next_step()
            next_agent_name = plan.get("next_action")
            next_reason = plan.get("reason")
            
            self.state.log_event("Supervisor", f"Decision: {next_agent_name} ({next_reason})")
    
            if next_agent_name == "FINISH":
                return False
            
            if next_agent_name == "ERROR":
                self.state.set_error("Supervisor: Missing Gemini API Key.")
                return False
                
            self.state.update_context("supervisor_phase", "EXECUTION")
            self.state.update_context("supervisor_next_agent", next_agent_name)
            return True

        elif phase == "EXECUTION":
            next_agent_name = self.state.get_context("supervisor_next_agent")
            agent = self.agents.get(next_agent_name)
            
            if agent:
                try:
                    agent.execute()
                except Exception as e:
                    self.state.set_error(f"Agent {next_agent_name} crashed: {e}")
            
            self.state.update_context("supervisor_phase", "PLANNING")
            self.state.update_context("supervisor_next_agent", None)
            return True
            
        return False
