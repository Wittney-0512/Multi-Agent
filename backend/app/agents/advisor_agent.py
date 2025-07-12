from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent


class AdvisorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位友善的顾问。
你的角色是提供建设性的建议和支持性的反馈。
当用户提出问题时，你应该尽可能给出有帮助的解答。
保持积极的态度，并尝试找出问题的最佳解决方案。"""
        super().__init__("顾问", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 顾问几乎总是回应
        return True
    
    def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
        
        user_message = global_context[-1].get("content", "")
        if not user_message:
            return None
            
        # 简单模拟回复生成
        return f"作为顾问，我认为这是一个很好的问题。我建议你可以尝试以下方法解决这个问题..."