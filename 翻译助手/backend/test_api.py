import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL")

print(f"Testing API with Key: {api_key[:8]}***")
print(f"Base URL: {base_url}")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

try:
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "user", "content": "你好，测试一下连接。"}
        ],
        temperature=0.3,
    )
    print("\nAPI Response Success:")
    print(completion.choices[0].message.content)
except Exception as e:
    print("\nAPI Call Failed:")
    print(e)
