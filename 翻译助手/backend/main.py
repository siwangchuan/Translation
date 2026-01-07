import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles # 新增
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI()

# 允许跨域请求，以便前端可以访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 新增：让后端同时托管前端静态文件 ---
# 1. 挂载 frontend 目录，用于访问样式或其他静态资源（如果有）
# 获取当前文件所在目录的父目录中的 frontend 文件夹绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")

# 2. 根路径直接返回 HTML 页面
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
# ---------------------------------------

# 配置 OpenAI 客户端 (使用阿里云 DashScope)
api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL")

if not api_key:
    raise ValueError("API Key is missing. Please check .env file.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=60.0, # 设置更长的超时时间
    max_retries=3 # 增加重试机制
)

class TranslateRequest(BaseModel):
    text: str

class TranslateResponse(BaseModel):
    translation: str
    keywords: list[str]

@app.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")

    prompt = f"""
    请将以下中文内容翻译成英文，并提取3个英文关键词。
    
    中文内容: "{request.text}"
    
    请务必只返回标准的 JSON 格式，不要包含任何 Markdown 标记或其他文本。
    格式要求:
    {{
        "translation": "翻译后的英文内容",
        "keywords": ["关键词1", "关键词2", "关键词3"]
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="qwen-turbo", # 使用通义千问模型
            messages=[
                {"role": "system", "content": "你是一个专业的翻译助手，擅长中译英及提取关键信息。请始终以纯 JSON 格式回复。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        content = completion.choices[0].message.content.strip()
        
        # 处理可能存在的 markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        result = json.loads(content)
        
        return TranslateResponse(
            translation=result.get("translation", ""),
            keywords=result.get("keywords", [])
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse model response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
