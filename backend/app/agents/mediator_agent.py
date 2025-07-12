from typing import List, Dict, Optional, Any
from .base_agent import BaseAgent

class MediatorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """你是一位协调者，名字就是"协调者"。
你的角色是总结其他Agent的观点并寻找共识。
当讨论进行时，你应该：
- 识别各方观点中的共同点
- 调和不同意见之间的冲突
- 提供中立的总结
- 引导讨论朝着建设性方向发展
- 在需要时提出折中方案

保持公正客观，不偏向任何一方观点。
请注意，你是多个AI助手中的一个，专注于协调角色，简明扼要地回答。"""
        super().__init__("协调者", system_prompt)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        # 协调者通常在其他Agent至少有两个回复后才回应
        if not global_context:
            return False
            
        # 获取最近的消息
        recent_messages = global_context[-10:] if len(global_context) > 10 else global_context
        
        # 计算不同Agent的回复数量
        agent_responses = {}
        for msg in recent_messages:
            if msg["role"] == "assistant" and "name" in msg:
                agent_name = msg["name"]
                agent_responses[agent_name] = agent_responses.get(agent_name, 0) + 1
        
        # 如果至少有两个不同的Agent回复，协调者应该回应
        if len(agent_responses) >= 2:
            return True
            
        # 如果用户明确要求总结或协调，也应回应
        latest_user_messages = [msg for msg in reversed(global_context) if msg["role"] == "user"]
        if not latest_user_messages:
            return False
            
        user_message = latest_user_messages[0]["content"].lower()
        keywords = ["总结", "协调", "意见", "建议", "综合", "折中", "共识"]
        
        return any(keyword in user_message for keyword in keywords)
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        if not global_context:
            return None
        
        messages = self.prepare_messages(global_context)
        return await self.openai_client.generate_completion(messages)