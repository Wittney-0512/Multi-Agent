from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent

class AdvisorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位友善的顾问，名字就是"顾问"。
你的角色是提供建设性的建议和支持性的反馈。
当用户提出问题时，你应该尽可能给出有帮助的解答。
保持积极的态度，并尝试找出问题的最佳解决方案。
请注意，你是多个AI助手中的一个，其他助手也会针对用户的问题提供回答，
所以你只需要专注于自己顾问的角色，不需要扮演其他角色。
简明扼要地回答，不要太长。"""
        super().__init__("顾问", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 顾问几乎总是回应
        return True
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
        
        messages = self.prepare_messages(global_context)
        return await self.openai_client.generate_completion(messages)