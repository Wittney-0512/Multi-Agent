from enum import Enum
from typing import List, Dict, Any, Tuple
import asyncio

class DiscussionStrategy(Enum):
    ROUNDTABLE = "roundtable"  # 轮询式讨论
    # 未来可扩展更多策略
    # DEBATE = "debate"        # 辩论式讨论
    # COLLABORATIVE = "collaborative"  # 协作式讨论

class DiscussionStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str, agents, **kwargs):
        if strategy_type == DiscussionStrategy.ROUNDTABLE.value:
            return RoundtableDiscussionStrategy(agents, **kwargs)
        # 未来添加其他策略
        raise ValueError(f"未支持的讨论策略: {strategy_type}")

class RoundtableDiscussionStrategy:
    """轮询式讨论策略：每个Agent在每轮中至多发言一次"""
    
    def __init__(self, agents, max_rounds=3):
        self.agents = agents
        self.max_rounds = max_rounds
        self.current_round = 0
    
    async def next_round(self, global_context) -> Tuple[List[Dict], bool]:
        """执行下一轮讨论，返回回复列表和讨论是否结束"""
        self.current_round += 1
        if self.current_round > self.max_rounds:
            return [], True  # 返回空回复列表和讨论结束标志
        
        print(f"开始执行第{self.current_round}轮讨论...")
        
        # 轮询所有Agent
        responses = []
        has_response = False
        
        # 收集所有应回应的Agent的任务
        tasks = []
        for agent in self.agents:
            if await agent.should_respond_in_discussion(global_context, self.current_round):
                task = self._get_agent_response(agent, global_context)
                tasks.append(task)
        
        # 并行等待所有回应
        if tasks:
            agent_responses = await asyncio.gather(*tasks)
            responses = [r for r in agent_responses if r]
            has_response = len(responses) > 0
        
        # 如果没有任何Agent回应，或者已达到最大轮次，结束讨论
        discussion_ended = (not has_response) or (self.current_round >= self.max_rounds)
        
        if discussion_ended:
            print(f"讨论结束，总共进行了{self.current_round}轮")
        
        return responses, discussion_ended
    
    async def _get_agent_response(self, agent, global_context):
        """获取单个Agent在讨论中的回应"""
        try:
            response_content = await agent.generate_discussion_response(global_context, self.current_round)
            if not response_content:
                return None
                
            return {
                "agent_name": agent.name,
                "content": response_content,
                "round": self.current_round
            }
        except Exception as e:
            print(f"获取Agent {agent.name}在讨论中的回应失败: {e}")
            return None