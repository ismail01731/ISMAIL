from typing import Any, Dict
class ActionRouter:
    def __init__(self):
        self.allowed_actions = {
            "open_app",
            "open_settings",
            "make_call",
            "send_message",
            "create_note",
            "emergency_alert",
        }
        self.sensitive_actions = {
            "make_call",
            "send_message",
            "emergency_alert",
        }
    def detect_action(self, text: str) -> Dict[str, Any]:
        if not text:
            return {
                "action": "none",
                "text": "",
                "confidence": 0.0,
            }
        command = text.strip().lower()
        # Specific actions first.
        # This prevents "call emergency contact" from
        # being incorrectly classified as emergency_alert.
        if "call" in command or "phone" in command:
            return {
                "action": "make_call",
                "text": text,
                "confidence": 0.85,
            }
        if "message" in command or "sms" in command:
            return {
                "action": "send_message",
                "text": text,
                "confidence": 0.85,
            }
        if "emergency" in command:
            return {
                "action": "emergency_alert",
                "text": text,
                "confidence": 0.95,
            }
        if "settings" in command:
            return {
                "action": "open_settings",
                "text": text,
                "confidence": 0.90,
            }
        if "open" in command:
            return {
                "action": "open_app",
                "text": text,
                "confidence": 0.70,
            }
        if "note" in command or "remember" in command:
            return {
                "action": "create_note",
                "text": text,
                "confidence": 0.80,
            }
        return {
            "action": "none",
            "text": text,
            "confidence": 0.0,
        }
    def is_allowed(self, action: str) -> bool:
        return action in self.allowed_actions
    def route(self, text: str) -> Dict[str, Any]:
        result = self.detect_action(text)
        if result["action"] == "none":
            result["allowed"] = False
            result["requires_confirmation"] = False
            return result
        result["allowed"] = self.is_allowed(
            result["action"]
        )
        result["requires_confirmation"] = (
            result["action"] in self.sensitive_actions
        )
        return result
action_router = ActionRouter()
