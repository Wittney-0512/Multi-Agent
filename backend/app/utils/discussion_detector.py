import json
import re
from app.utils.openai_client import OpenAIClient

class DiscussionDetector:
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
    
    async def detect_discussion_needed(self, user_input: str) -> dict:
        """判断用户输入是否需要Agent间讨论"""
        
        if self.openai_client:
            prompt = f"""
        请仔细分析以下用户输入，判断用户意图并评估话题复杂性。

    用户输入: "{user_input}"

    可能的AI助手角色: ["顾问", "批评者", "创新者", "协调者"]

    请分析:
    1. 用户是否希望AI助手之间进行讨论?
    2. 用户是否明确指定了特定角色回答?
    3. 如果指定了特定角色，是哪个角色?
    4. 话题的复杂性程度（影响讨论轮数）

    对于复杂性评估，请考虑:
    - 话题是否有争议性/多角度
    - 是否需要深入探讨
    - 是否涉及多领域知识
    - 是否需要辩证思考

    基于复杂性，建议讨论轮数:
    - 简单话题: 2轮
    - 中等复杂: 3轮
    - 较复杂话题: 4轮
    - 非常复杂: 5轮（最大值）

    请以JSON格式返回分析结果:
    {{
    "needs_discussion": true/false,       // 是否需要讨论
    "specified_agents": ["角色名"],        // 指定回答角色
    "excluded_agents": ["角色名"],         // 排除角色
    "topic_complexity": "简单/中等/较复杂/非常复杂", // 话题复杂性评估
    "suggested_rounds": 2-5,              // 建议讨论轮数(2-5)
    "confidence": 0.1-1.0,                // 判断置信度
    "reason": "简要解释判断理由",          // 判断理由
    "extract_topic": true/false           // 是否需要提取主题
    }}
    """
            try:
                response = await self.openai_client.generate_completion([
                    {"role": "system", "content": "你是一个专门分析用户意图的助手，只返回JSON格式回复，不要有其他内容。"},
                    {"role": "user", "content": prompt}
                ])
                
                import json
                import re
                
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    return result
                    
            except Exception as e:
                print(f"AI判断讨论需求失败: {e}")
        
        # 退化方案：简单的关键词检测（仅在AI分析失败时使用）
        discussion_keywords = ["讨论", "商量", "你们商量", "你们讨论", "内部沟通"]
        reject_keywords = ["不要讨论", "不需要讨论", "无需讨论", "直接回答"]
        
        if any(keyword in user_input for keyword in reject_keywords):
            return {
                "needs_discussion": False,
                "confidence": 0.7,
                "reason": "关键词检测：用户拒绝讨论",
                "suggested_rounds": 0
            }
        
        if any(keyword in user_input for keyword in discussion_keywords):
            return {
                "needs_discussion": True,
                "confidence": 0.7,
                "reason": "关键词检测：触发讨论关键词",
                "suggested_rounds": 3
            }
        
        # 默认不需要讨论
        return {
            "needs_discussion": False,
            "confidence": 0.5,
            "reason": "默认模式：无明确讨论意图",
            "suggested_rounds": 0
        }
    
    # 主题提取
    async def extract_discussion_topic(self, user_input: str) -> str:
        """从用户输入中提取真正的讨论主题"""
        if not self.openai_client:
            # 如果没有AI客户端，简单处理：移除常见的讨论请求词
            remove_patterns = [
                "请讨论", "你们讨论", "讨论一下", "商量一下", 
                "一起分析", "达成共识"
            ]
            topic = user_input
            for pattern in remove_patterns:
                topic = topic.replace(pattern, "")
            return topic.strip()
        
        prompt = f"""
    提取以下用户输入中的真正讨论主题，忽略讨论指令部分。

    用户输入: "{user_input}"

    例如，如果输入是"请大家讨论一下气候变化的影响"，应该提取的主题是"气候变化的影响"。
    请直接返回提取的主题，无需其他解释。
    """
        try:
            topic = await self.openai_client.generate_completion([
                {"role": "system", "content": "你是一个专门提取讨论主题的助手，只返回提取的主题，不要有其他内容。"},
                {"role": "user", "content": prompt}
            ])
            return topic.strip()
        except Exception as e:
            print(f"提取讨论主题失败: {e}")
            return user_input