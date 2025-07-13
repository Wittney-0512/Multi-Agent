import asyncio
import logging
import openai
from openai import OpenAI
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info(f"OpenAI客户端初始化，API密钥长度: {len(settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else 0}")
        
    async def generate_completion(self, messages, model=None):
        """异步包装同步API调用"""
        try:
            logger.info(f"开始调用OpenAI API, 模型: {model or settings.OPENAI_MODEL}")
            # 使用线程池执行器来非阻塞地运行同步API调用
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model or settings.OPENAI_MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
            )
            logger.info("OpenAI API调用成功")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API调用错误: {str(e)}", exc_info=True)
            return f"抱歉，生成回复时发生错误: {str(e)}"