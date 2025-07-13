import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 测试API连接
api_key = os.getenv("OPENAI_API_KEY")
print(f"API密钥长度: {len(api_key) if api_key else 0}")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        temperature=0.7,
        max_tokens=50
    )
    print("API调用成功!")
    print(f"回复: {response.choices[0].message.content}")
except Exception as e:
    print(f"API调用失败: {str(e)}")