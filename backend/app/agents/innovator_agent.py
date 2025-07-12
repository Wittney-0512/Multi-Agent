from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent


class InnovatorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位创新者。
你的角色是提供创新性的解决方案和新颖的视角。
当讨论进行时，你应该思考突破性的方法和未被考虑的可能性。
鼓励创造性思维，并尝试突破常规思维的局限。"""
        super().__init__("创新者", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 创新者对创意相关问题更感兴趣
        if not global_context:
            return False
            
        user_message = global_context[-1].get("content", "").lower()
        
        # 如果用户提问中包含创意、新想法等关键词，创新者更可能回应
        keywords = ["新想法", "创意", "创新", "不同方法", "另一种思路", "可能性"]
        return any(keyword in user_message for keyword in keywords)
    
    def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
            
        user_message = global_context[-1].get("content", "")
        if not user_message:
            return None
            
        # 简单模拟回复生成
        return f"作为创新者，我想提出一个全新的视角来看待这个问题..."