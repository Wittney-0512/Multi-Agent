from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位专业的批评者，名字就是"批评者"。
你的角色是提供建设性批评和指出潜在问题，帮助用户看到他们可能忽略的盲点。
当讨论进行时，你应该：
- 评估想法的弱点、漏洞和潜在风险
- 提出合理的疑问和质疑
- 挑战不合理的假设
- 指出逻辑缺陷
- 思考可能被忽视的反面观点

保持客观专业，重点是改进和完善想法，而不是简单否定。批评应当有针对性和具体建设性。
请注意，你是多个AI助手中的一个，其他助手会提供支持和创新视角，
所以你应专注于批评者角色，不需要扮演其他角色或提供全面解决方案。
简明扼要地回答，不要太长。"""
        super().__init__("批评者", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 批评者不是对每个问题都回应
        if not global_context:
            return False
            
        # 获取最新的用户消息
        latest_user_messages = [msg for msg in reversed(global_context) if msg["role"] == "user"]
        if not latest_user_messages:
            return False
            
        user_message = latest_user_messages[0]["content"].lower()
        
        # 如果用户明确要求批评、反馈或评估，批评者应该回应
        explicit_keywords = ["批评", "缺点", "问题", "风险", "不足", "评价", "评估", "反馈"]
        if any(keyword in user_message for keyword in explicit_keywords):
            return True
        
        # 如果用户在讨论计划、想法、观点或方案，批评者也可能回应
        implicit_keywords = ["计划", "想法", "方案", "观点", "认为", "如何", "怎么样", "可行性", "策略"]
        if any(keyword in user_message for keyword in implicit_keywords):
            # 对于这类问题，70%的概率回应
            import random
            return random.random() < 0.7
        
        # 对于一般性问题，30%的概率回应
        import random
        return random.random() < 0.3
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
        
        messages = self.prepare_messages(global_context)
        return await self.openai_client.generate_completion(messages)