import asyncio
import logging
from typing import List, Dict, Any
from .advisor_agent import AdvisorAgent
from .critic_agent import CriticAgent
from .innovator_agent import InnovatorAgent
from .mediator_agent import MediatorAgent
from .base_agent import BaseAgent
from app.utils.intent_analyzer import IntentAnalyzer

class AgentManager:
    def __init__(self):
        self.agents = [
            AdvisorAgent(),
            CriticAgent(),
            InnovatorAgent(),
            MediatorAgent()
        ]
        self.global_context = []
        self.intent_analyzer = IntentAnalyzer()
    
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
        
        # 获取最新用户消息
        latest_user_messages = [msg for msg in reversed(self.global_context) if msg["role"] == "user"]
        if not latest_user_messages:
            return []
            
        user_message = latest_user_messages[0]["content"]
        
        # 分析用户意图
        available_agents = [agent.name for agent in self.agents]
        intent_result = await self.intent_analyzer.analyze_speaker_intent(user_message, available_agents)
        
        print(f"用户输入: '{user_message}'")
        print(f"意图分析结果: {intent_result}")
        
        # 根据意图结果筛选应该回应的Agent
        for agent in self.agents:
            should_speak = agent.name in intent_result.get("should_speak", [])
            should_not_speak = agent.name in intent_result.get("should_not_speak", [])
            
            if should_speak and not should_not_speak:
                # 确定应该说话
                task = self._process_agent_response(agent)
                tasks.append(task)
            elif not should_speak and not should_not_speak:
                # 没有明确指定，使用Agent自己的判断逻辑
                if agent.should_respond(self.global_context):
                    task = self._process_agent_response(agent)
                    tasks.append(task)
        
        # 并行等待所有任务完成
        responses = await asyncio.gather(*tasks)
        
        # 过滤掉空回复
        return [r for r in responses if r]
    
    async def _process_agent_response(self, agent: BaseAgent) -> Dict[str, Any]:
        """处理单个agent的响应"""
        try:
            response_content = await agent.generate_response(self.global_context)
            
            if not response_content:
                return None
            
            # 添加身份检查 - 新增代码
            if response_content and ("作为" in response_content or "我是" in response_content):
                wrong_identities = []
                for a in self.agents:
                    if a.name != agent.name:
                        if f"作为{a.name}" in response_content or f"我是{a.name}" in response_content:
                            wrong_identities.append(a.name)
                
                if wrong_identities:
                    # 检测到身份混淆，进行修正
                    print(f"检测到{agent.name}身份混淆，提及了: {wrong_identities}")
                    correction_prompt = f"""你是{agent.name}，请重写以下回复，确保:
1. 不要说"作为{', '.join(wrong_identities)}"
2. 不要说"我是{', '.join(wrong_identities)}"
3. 不要代表其他角色发言
4. 保持原始回复的主要内容和建议

原回复:
{response_content}"""
                    response_content = await agent.openai_client.generate_completion([
                        {"role": "system", "content": agent.system_prompt},
                        {"role": "user", "content": correction_prompt}
                    ])
                    print(f"修正后回复: {response_content[:50]}...")
                
            response = {
                "agent_name": agent.name,
                "content": response_content
            }
            
            # 添加到全局上下文
            self.global_context.append({
                "role": "assistant",
                "name": agent.name,
                "agent_role": agent.name,  # 添加自定义字段明确Agent角色
                "content": response_content
            })
            
            # 添加到Agent自己的私有上下文
            agent.add_to_private_context({
                "role": "assistant",
                "agent_role": agent.name,
                "content": response_content
            })
            
            return response
        except Exception as e:
            logging.error(f"Agent {agent.name}响应处理错误: {str(e)}", exc_info=True)
            return {
                "agent_name": agent.name,
                "content": f"处理响应时发生错误: {str(e)}"
            }