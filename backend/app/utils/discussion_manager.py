import asyncio
from typing import List, Dict, Any, Optional
from app.utils.discussion_strategies import DiscussionStrategy, DiscussionStrategyFactory

class DiscussionManager:
    """讨论管理器：负责执行和管理Agent之间的讨论流程"""
    
    def __init__(self, agent_manager):
        """初始化讨论管理器
        
        Args:
            agent_manager: Agent管理器实例，用于访问agents和上下文
        """
        self.agent_manager = agent_manager
    
    async def run_discussion_cycle(self, user_input: str, strategy_type: str = DiscussionStrategy.ROUNDTABLE.value, max_rounds: int = 3):
        """执行一个完整的讨论周期
        
        Args:
            user_input: 用户输入，将作为讨论的主题
            strategy_type: 讨论策略类型
            max_rounds: 最大讨论轮数
            
        Returns:
            List[Dict]: 所有回复的列表，包含讨论中所有Agent的发言
        """
        # 将用户输入添加到上下文
        self.agent_manager.add_user_message(user_input)
        
        print(f"开始执行讨论周期，策略：{strategy_type}，最大轮数：{max_rounds}")
        
        # 创建讨论策略
        strategy = DiscussionStrategyFactory.create_strategy(
            strategy_type, 
            self.agent_manager.agents,
            max_rounds=max_rounds
        )
        
        all_responses = []
        discussion_ended = False
        
        # 执行多轮讨论
        while not discussion_ended:
            # 执行一轮讨论
            round_responses, discussion_ended = await strategy.next_round(
                self.agent_manager.global_context
            )
            
            if not round_responses:
                print("本轮无Agent回应，讨论结束")
                break
                
            print(f"第{strategy.current_round}轮讨论收到{len(round_responses)}个回应")
                
            # 将本轮回应添加到全局上下文和Agent私有上下文
            for response in round_responses:
                agent_name = response["agent_name"]
                content = response["content"]
                round_num = response["round"]
                
                # 添加到全局上下文
                self.agent_manager.global_context.append({
                    "role": "assistant",
                    "name": agent_name,
                    "agent_role": agent_name,
                    "content": content,
                    "is_discussion": True,  # 标记这是讨论中的回应
                    "discussion_round": round_num
                })
                
                # 添加到相应Agent的私有上下文
                for agent in self.agent_manager.agents:
                    if agent.name == agent_name:
                        agent.add_to_private_context({
                            "role": "assistant",
                            "agent_role": agent_name,
                            "content": content,
                            "is_discussion": True,
                            "discussion_round": round_num
                        })
                
                # 添加到返回的响应列表
                all_responses.append(response)
        
        print(f"讨论结束，共产生{len(all_responses)}个回应")
        return all_responses
    
    async def maybe_add_summary(self, discussion_responses: List[Dict]) -> Optional[Dict]:
        """可选：在讨论结束后添加总结
        
        Args:
            discussion_responses: 讨论中的所有回应
            
        Returns:
            Dict|None: 总结回应，如果不需要总结则返回None
        """
        # 这里可以选择一个Agent（如协调者）来提供讨论总结
        # 暂时先简单实现，后续可以扩展
        for agent in self.agent_manager.agents:
            if agent.name == "协调者":
                # 由协调者生成总结
                try:
                    summary = await agent.generate_discussion_summary(
                        self.agent_manager.global_context,
                        discussion_responses
                    )
                    
                    if summary:
                        # 添加到全局上下文
                        self.agent_manager.global_context.append({
                            "role": "assistant",
                            "name": agent.name,
                            "agent_role": agent.name,
                            "content": summary,
                            "is_discussion": True,
                            "is_summary": True
                        })
                        
                        # 添加到Agent私有上下文
                        agent.add_to_private_context({
                            "role": "assistant",
                            "agent_role": agent.name,
                            "content": summary,
                            "is_discussion": True,
                            "is_summary": True
                        })
                        
                        return {
                            "agent_name": agent.name,
                            "content": summary,
                            "is_summary": True
                        }
                except Exception as e:
                    print(f"生成讨论总结时出错: {e}")
                    return None
        
        return None