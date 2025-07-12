import asyncio
import logging
from typing import List, Dict, Any
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
    
    async def get_responses(self) -> List[Dict[str, Any]]:
        """异步获取所有应该回应的Agent的回复"""
        tasks = []
        
        for agent in self.agents:
            if agent.should_respond(self.global_context):
                # 为每个应响应的agent创建异步任务
                task = self._process_agent_response(agent)
                tasks.append(task)
        
        # 并行等待所有任务完成
        responses = await asyncio.gather(*tasks)
        
        # 过滤掉空回复
        return [r for r in responses if r]
    
    async def _process_agent_response(self, agent: BaseAgent) -> Dict[str, Any]:
        """处理单个agent的响应"""
        try:
            logging.info(f"开始处理Agent {agent.name}的响应")
            response_content = await agent.generate_response(self.global_context)
            
            if not response_content:
                logging.warning(f"Agent {agent.name}返回空响应")
                return None
                
            response = {
                "agent_name": agent.name,
                "content": response_content
            }
            
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
            
            logging.info(f"Agent {agent.name}响应处理完成")
            return response
        except Exception as e:
            logging.error(f"Agent {agent.name}响应处理错误: {str(e)}", exc_info=True)
            return {
                "agent_name": agent.name,
                "content": f"处理响应时发生错误: {str(e)}"
            }