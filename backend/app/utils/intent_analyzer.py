# 用户意图分析
from app.utils.openai_client import OpenAIClient

class IntentAnalyzer:
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    async def analyze_speaker_intent(self, user_message, available_agents):
        """分析用户消息中关于哪些Agent应该说话的意图"""
        prompt = f"""
你是一个精确的意图分析助手。请仔细分析以下用户消息，判断用户希望哪些AI助手回复。

可用的AI助手有: {', '.join(available_agents)}
每个助手都有明确的角色和职责:
- 顾问：提供建议和支持性反馈
- 批评者：提供批判性思考和指出潜在问题
- 创新者：提供创新性解决方案和新颖视角
- 协调者：总结其他Agent观点并寻找共识

用户消息: "{user_message}"

请特别注意:
1. "只有X"表示只允许X回复，其他所有助手都不应回复
2. "X不要说话"表示X明确不应回复
3. 如用户指明某助手应该或不应该回复，必须严格遵循
4. 如果不确定，宁可返回所有助手都可以回复

以JSON格式返回分析结果:
{{
  "should_speak": ["应该回复的助手名称"],
  "should_not_speak": ["不应回复的助手名称"],
  "confidence": 0.9  // 判断的置信度(0-1)
}}

只返回JSON，不要有其他文字。
"""
        
        try:
            response = await self.openai_client.generate_completion([
                {"role": "system", "content": "你是一个意图分析助手，专门分析用户希望哪些AI助手回复。只返回JSON格式。"},
                {"role": "user", "content": prompt}
            ])
            
            import json
            # 提取JSON部分
            try:
                result = json.loads(response)
                return result
            except:
                # 如果返回的不是纯JSON，尝试提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    return result
                else:
                    return {"should_speak": available_agents, "should_not_speak": [], "confidence": 0}
                
        except Exception as e:
            print(f"意图分析错误: {e}")
            # 出错时，默认所有Agent都可以回复
            return {"should_speak": available_agents, "should_not_speak": [], "confidence": 0}