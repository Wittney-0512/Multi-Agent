from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from app.utils.openai_client import OpenAIClient
import random


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
        """判断当前Agent是否应该回应，根据自身特性"""
        # 默认实现，子类可以重写
        return True
    
    def prepare_messages(self, global_context: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """准备发送给API的消息列表，包含系统提示和上下文"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # 添加全局上下文中的消息，但过滤出相关消息
        for msg in global_context:
            if msg["role"] == "user":
                # 用户消息总是包含
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                # 只包含当前Agent的回复或无Agent标识的回复
                if "name" in msg and msg["name"] == self.name:
                    messages.append({"role": "assistant", "content": msg["content"]})
                # 也可以选择包含其他Agent的回复，但需要明确标识
                # elif "name" in msg and msg["name"] != self.name:
                #     messages.append({"role": "user", "content": f"{msg['name']}: {msg['content']}"})
        
        return messages
    
    async def generate_response(self, global_context: List[Dict[str, Any]]) -> Optional[str]:
        """生成回应 - 由子类实现"""
        pass

    # 引入讨论
    async def should_respond_in_discussion(self, global_context: List[Dict[str, Any]], current_round: int) -> bool:
        """判断Agent是否应该在讨论中回应
        Args:
        global_context: 全局上下文历史
        current_round: 当前讨论轮次
        
        Returns:
            bool: 是否应该回应
        """
        # 默认实现：在第一轮所有人都回应，后续轮次有50%概率回应
        if current_round == 1:
            return True
        return random.random() > 0.5

    async def generate_discussion_response(self, global_context: List[Dict[str, Any]], current_round: int) -> Optional[str]:
        """生成Agent在讨论中的回应
        Args:
        global_context: 全局上下文历史
        current_round: 当前讨论轮次
        
        Returns:
            str: 生成的回应内容
        """
        # 构建特殊提示，强调这是Agent间的讨论
        discussion_messages = self.prepare_discussion_messages(global_context, current_round)
        return await self.openai_client.generate_completion(discussion_messages)

    def prepare_discussion_messages(self, global_context: List[Dict[str, Any]], current_round: int) -> List[Dict[str, str]]:
        """准备用于讨论的消息列表
        Args:
        global_context: 全局上下文历史
        current_round: 当前讨论轮次
        
        Returns:
            List[Dict]: 准备好的消息列表
        """
        # 基础系统提示
        system_prompt = f"""{self.system_prompt}

    现在你正在与其他AI助手进行内部讨论，这是第{current_round}轮讨论。
    你应该：
    1. 保持你的角色特点
    2. 参考之前的发言
    3. 提出你的观点或回应其他助手
    4. 简明扼要地表达想法
    5. 记住你是{self.name}，不要混淆身份

    请不要说"作为{self.name}"，直接以你的角色身份发言即可。
    """

        messages = [{"role": "system", "content": system_prompt}]

        # 提取最后一条用户消息作为讨论主题
        user_messages = [msg for msg in global_context if msg["role"] == "user"]
        if user_messages:
            latest_user_message = user_messages[-1]
            messages.append({"role": "user", "content": f"讨论主题: {latest_user_message['content']}"})
    
        
        # 添加上下文中的内容，标记是谁说的
        discussion_history = []
        for msg in global_context:
            if msg["role"] == "assistant" and "name" in msg and msg.get("is_discussion", False):
                agent_name = msg["name"]
                discussion_history.append(f"{agent_name}: {msg['content']}")
        
        if discussion_history:
            messages.append({
                "role": "user", 
                "content": f"之前的讨论:\n" + "\n".join(discussion_history)
            })
        
        return messages

    async def generate_discussion_summary(self, global_context: List[Dict[str, Any]], discussion_responses: List[Dict]) -> Optional[str]:
        """生成讨论总结
        
        Args:
            global_context: 全局上下文
            discussion_responses: 讨论中的所有回应
            
        Returns:
            str: 总结内容
        """
        # 默认实现为空，由具体Agent类（如协调者）来实现
        return None