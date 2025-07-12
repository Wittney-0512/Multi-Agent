from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from app.utils.openai_client import OpenAIClient

class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.private_context: List[Dict[str, Any]] = []
        self.openai_client = OpenAIClient()
    
    def add_to_private_context(self, message: Dict[str, Any]):
        """添加消息到私有上下文"""
        self.private_context.append(message)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        """判断当前Agent是否应该回应
        默认总是回应，子类可以覆盖此方法以实现特定逻辑
        """
        return True
    
    def prepare_messages(self, global_context: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """准备发送给API的消息列表，包含系统提示和上下文"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # 添加全局上下文中的用户消息
        for msg in global_context:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant" and msg.get("name") == self.name:
                # 只添加当前Agent的回复
                messages.append({"role": "assistant", "content": msg["content"]})
        
        return messages
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        """生成回应 - 由子类实现"""
        pass