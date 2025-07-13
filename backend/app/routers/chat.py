from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.agents.agent_manager import AgentManager
from app.utils.discussion_detector import DiscussionDetector
from app.utils.discussion_manager import DiscussionManager
from app.utils.openai_client import OpenAIClient

router = APIRouter(tags=["chat"])

# 保存全局AgentManager实例
agent_manager = AgentManager()

# 创建讨论检测器和管理器
discussion_detector = DiscussionDetector(openai_client=OpenAIClient())
discussion_manager = DiscussionManager(agent_manager)


class UserMessageRequest(BaseModel):
    content: str


class AgentResponse(BaseModel):
    agent_name: str
    content: str
    round: Optional[int] = None  # 用于标识讨论轮次
    is_summary: bool = False     # 是否是讨论总结


class ChatResponse(BaseModel):
    responses: List[AgentResponse]
    is_discussion: bool = False  # 标记是否是讨论模式

# 支持用户直接请求Agent讨论
class DiscussionRequest(BaseModel):
    topic: str
    max_rounds: int = 3
    strategy: str = "roundtable"

@router.get("/context")
async def get_context():
    """获取当前上下文状态"""
    context_info = {
        "global_context_length": len(agent_manager.global_context),
        "global_context": agent_manager.global_context,
        "agents": {}
    }
    
    for agent in agent_manager.agents:
        context_info["agents"][agent.name] = {
            "private_context_length": len(agent.private_context),
            "private_context": agent.private_context
        }
    
    return context_info


@router.post("/chat", response_model=ChatResponse)
async def chat(request: UserMessageRequest):
    try:
        # 检测用户意图
        intent_result = await discussion_detector.detect_discussion_needed(request.content)
        print(f"用户意图分析结果: {intent_result}")
        
        responses = []
        is_discussion_mode = False

        # 添加用户消息到全局上下文
        agent_manager.add_user_message(request.content)
        
        if intent_result.get("needs_discussion", False):
            # 讨论模式处理逻辑
            print(f"检测到讨论需求")
            is_discussion_mode = True

            # 提取讨论主题
            discussion_topic = request.content
            if intent_result.get("extract_topic", True):
                discussion_topic = await discussion_detector.extract_discussion_topic(request.content)
                print(f"提取的讨论主题: {discussion_topic}")
            
            # 执行讨论流程
            discussion_responses = await discussion_manager.run_discussion_cycle(
                discussion_topic, 
                max_rounds=intent_result.get("suggested_rounds", 3)
            )
            
            # 转换为响应格式
            for resp in discussion_responses:
                responses.append(AgentResponse(
                    agent_name=resp["agent_name"],
                    content=resp["content"],
                    round=resp.get("round"),
                    is_summary=resp.get("is_summary", False)
                ))
            
            # 可选：添加讨论总结
            summary = await discussion_manager.maybe_add_summary(discussion_responses)
            if summary:
                responses.append(AgentResponse(
                    agent_name=summary["agent_name"],
                    content=summary["content"],
                    is_summary=True
                ))

        elif len(intent_result.get("specified_agents", [])) > 0:
            # 指定Agent回答模式
            specified_agents = intent_result["specified_agents"]
            print(f"用户指定的Agent: {specified_agents}")
            
            # 只调用指定的Agent
            for agent in agent_manager.agents:
                if agent.name in specified_agents:
                    response = await agent_manager._process_agent_response(agent)
                    if response:
                        responses.append(AgentResponse(
                            agent_name=response["agent_name"],
                            content=response["content"]
                        ))
                
        else:
            # 原有的直接回复流程
            agent_manager.add_user_message(request.content)
            agent_responses = await agent_manager.get_responses()
            
            # 转换为响应格式
            for resp in agent_responses:
                responses.append(AgentResponse(
                    agent_name=resp["agent_name"],
                    content=resp["content"]
                ))
        
        return ChatResponse(
            responses=responses,
            is_discussion=is_discussion_mode
        )
        
    except Exception as e:
        print(f"处理聊天请求时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discussion/status")
async def get_discussion_status():
    """获取当前讨论状态（用于调试）"""
    discussion_messages = [
        msg for msg in agent_manager.global_context 
        if msg.get("is_discussion", False)
    ]
    
    return {
        "discussion_count": len(discussion_messages),
        "discussion_messages": discussion_messages
    }

# 支持用户直接请求Agent讨论
@router.post("/discussion", response_model=ChatResponse)
async def start_discussion(request: DiscussionRequest):
    """启动一个Agent讨论"""
    try:
        # 直接启动讨论，无需检测
        discussion_responses = await discussion_manager.run_discussion_cycle(
            request.topic, 
            strategy_type=request.strategy,
            max_rounds=request.max_rounds
        )
        
        # 转换为响应格式
        responses = []
        for resp in discussion_responses:
            responses.append(AgentResponse(
                agent_name=resp["agent_name"],
                content=resp["content"],
                round=resp.get("round"),
                is_summary=resp.get("is_summary", False)
            ))
        
        # 可选：添加讨论总结
        summary = await discussion_manager.maybe_add_summary(discussion_responses)
        if summary:
            responses.append(AgentResponse(
                agent_name=summary["agent_name"],
                content=summary["content"],
                is_summary=True
            ))
            
        return ChatResponse(
            responses=responses,
            is_discussion=True
        )
        
    except Exception as e:
        print(f"启动讨论时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))