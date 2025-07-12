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
    
    # 获取Agent回复
    responses = agent_manager.get_responses()
    
    return {"responses": responses}