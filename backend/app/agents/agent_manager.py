from typing import List, Dict, Any, Optional
from .advisor_agent import AdvisorAgent
from .critic_agent import CriticAgent
from .innovator_agent import InnovatorAgent
from .base_agent import BaseAgent


class AgentManager:
    def __init__(self):
        self.agents: List[BaseAgent] = [
            AdvisorAgent(),
            CriticAgent(),
            InnovatorAgent()
        ]
        self.global_context: List[Dict[str, Any]] = []
    
    def add_user_message(self, content: str):
        """添加用户消息到全局上下文"""
        message = {
            "role": "user",
            "content": content
        }
        self.global_context.append(message)
        
        # 同时添加到每个Agent的私有上下文
        for agent in self.agents:
            agent.add_to_private_context(message)
    
    def get_responses(self) -> List[Dict[str, Any]]:
        """获取所有应该回应的Agent的回复"""
        responses = []
        
        for agent in self.agents:
            if agent.should_respond(self.global_context):
                response_content = agent.generate_response(self.global_context)
                if response_content:
                    response = {
                        "agent_name": agent.name,
                        "content": response_content
                    }
                    responses.append(response)
                    
                    # 添加到全局上下文
                    self.global_context.append({
                        "role": "assistant",
                        "name": agent.name,
                        "content": response_content
                    })
                    
                    # 添加到Agent自己的私有上下文
                    agent.add_to_private_context({
                        "role": "assistant",
                        "content": response_content
                    })
        
        return responses