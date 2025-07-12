from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.agents.agent_manager import AgentManager

router = APIRouter(tags=["chat"])

# 保存全局AgentManager实例
agent_manager = AgentManager()


class UserMessageRequest(BaseModel):
    content: str


class AgentResponse(BaseModel):
    agent_name: str
    content: str


class ChatResponse(BaseModel):
    responses: List[AgentResponse]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: UserMessageRequest):
    # 添加用户消息
    agent_manager.add_user_message(request.content)
    
    # 异步获取Agent回复
    responses = await agent_manager.get_responses()
    
    return {"responses": responses}

# 获取当前上下文状态
@router.get("/context", response_model=dict)
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