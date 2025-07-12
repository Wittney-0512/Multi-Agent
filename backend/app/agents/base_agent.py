from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.private_context: List[Dict[str, Any]] = []
    
    def add_to_private_context(self, message: Dict[str, Any]):
        """添加消息到私有上下文"""
        self.private_context.append(message)
    
    def should_respond(self, global_context: List[Dict[str, Any]]) -> bool:
        """判断当前Agent是否应该回应
        默认总是回应，子类可以覆盖此方法以实现特定逻辑
        """
        return True
    
    @abstractmethod
    def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        """生成回应"""
        pass