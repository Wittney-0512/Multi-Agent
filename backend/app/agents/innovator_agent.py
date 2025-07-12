from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent

class InnovatorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位创新思维专家。
你的角色是提供创新性的解决方案、新颖的视角和突破性的思路。
当讨论进行时，你应该：
- 提出非常规的思考角度和创新方法
- 突破传统思维模式，提供创造性建议
- 发现问题中被忽略的机会
- 结合不同领域的知识，产生独特见解
- 思考"如果没有限制，可能的解决方案是什么？"

鼓励创造性思维，帮助用户拓展思路边界，不要被现有条件和假设所限制。
请注意，你是多个AI助手中的一个，其他助手会提供支持和批判视角，
所以你应专注于创新者角色，不需要扮演其他角色或评估风险。
简明扼要地回答，不要太长。"""
        super().__init__("创新者", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 创新者对创意相关问题更感兴趣
        if not global_context:
            return False
            
        # 获取最新的用户消息
        latest_user_messages = [msg for msg in reversed(global_context) if msg["role"] == "user"]
        if not latest_user_messages:
            return False
            
        user_message = latest_user_messages[0]["content"].lower()
        
        # 如果用户明确询问创新、新想法或不同思路，创新者应该回应
        explicit_keywords = ["创新", "新想法", "创意", "突破", "不同思路", "新方法", "可能性", "创造性"]
        if any(keyword in user_message for keyword in explicit_keywords):
            return True
        
        # 如果用户在讨论解决方案、改进或设计相关问题，创新者也可能回应
        implicit_keywords = ["如何", "怎样", "解决", "改进", "设计", "开发", "构思", "灵感", "想象"]
        if any(keyword in user_message for keyword in implicit_keywords):
            # 对于这类问题，80%的概率回应
            import random
            return random.random() < 0.8
        
        # 对于问题性质的提问，创新者通常也会有新视角
        question_keywords = ["为什么", "是什么", "可能吗"]
        if any(keyword in user_message for keyword in question_keywords):
            # 对于这类问题，50%的概率回应
            import random
            return random.random() < 0.5
            
        # 对于一般性问题，40%的概率回应
        import random
        return random.random() < 0.4
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
        
        messages = self.prepare_messages(global_context)
        return await self.openai_client.generate_completion(messages)