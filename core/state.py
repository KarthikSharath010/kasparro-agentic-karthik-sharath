import json
from datetime import datetime

class SharedState:
    def __init__(self):
        self._state = {
            "messages": [], # Log of agent interactions
            "artifacts": {}, # Final outputs (JSONs)
            "context": {},   # Intermediate data (raw questions, etc.)
            "status": "initialized",
            "errors": []
        }
    
    def update_context(self, key, value):
        self._state["context"][key] = value
        self.log_event("system", f"Updated context: {key}")

    def save_artifact(self, key, value):
        self._state["artifacts"][key] = value
        self.log_event("system", f"Saved artifact: {key}")

    def get_context(self, key):
        return self._state["context"].get(key)
    
    def get_artifact(self, key):
        return self._state["artifacts"].get(key)
    
    def get_all(self):
        return self._state
    
    def log_event(self, source, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "source": source,
            "message": message
        }
        self._state["messages"].append(entry)

    def set_error(self, error_message):
        self._state["errors"].append(error_message)
        self.log_event("error", error_message)
