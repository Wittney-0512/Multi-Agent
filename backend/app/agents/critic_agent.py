from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent


class CriticAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位批评者。
你的角色是提供批判性思考和指出潜在的问题。
当讨论进行时，你应该评估其中的弱点和漏洞。
保持客观，重点是改进和完善想法，而不是简单否定。"""
        super().__init__("批评者", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 批评者不是对每个问题都回应
        if not global_context:
            return False
            
        user_message = global_context[-1].get("content", "").lower()
        
        # 如果用户提问中包含请求反馈、评估等关键词，批评者更可能回应
        keywords = ["问题", "缺点", "评价", "如何改进", "批评", "反馈"]
        return any(keyword in user_message for keyword in keywords)
    
    def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
            
        user_message = global_context[-1].get("content", "")
        if not user_message:
            return None
            
        # 简单模拟回复生成
        return f"作为批评者，我注意到这个想法有几个潜在的问题需要解决..."