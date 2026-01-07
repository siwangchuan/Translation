# AI 翻译助手 — 项目说明与启动手册

这是一个轻量级的「AI 翻译助手」示例项目，包含后端（FastAPI）和前端（纯 HTML + JS）。后端调用兼容阿里云 DashScope 的通用大模型 API（在本示例中以 OpenAI SDK 的兼容接口方式使用）。

## 项目结构

- `backend/` — 后端服务
  - `main.py` — FastAPI 应用，暴露 `/translate` POST 接口
  - `.env` — 环境变量（存放 API Key、base_url）
  - `requirements.txt` — Python 依赖

- `frontend/` — 前端页面
  - `index.html` — 单页 HTML + JS，调用后端接口并展示结果

- `README.md` — 本说明文件

---

**主要功能**

- POST `/translate`：接收 `{ "text": "要翻译的中文内容" }`，返回 `{ "translation": "英文翻译结果", "keywords": ["关键词1","关键词2","关键词3"] }`。
- 前端页面提供输入框、翻译按钮、结果展示与复制功能。

---

## 先决条件

- Windows（本机为 Windows）或其他操作系统
- 安装了 Python 3.8+
- 建议使用虚拟环境（venv）隔离依赖

---

## 环境变量（必须）

在 `backend/.env` 中配置：

```
ALIYUN_API_KEY=sk-3a8dd7dda41b4964a6e29776f4155f0d
ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

注意：生产环境请不要把密钥直接写在仓库或公开位置。

---

## 安装依赖与运行（PowerShell 示例）

在项目根目录（`C:\Users\si\Desktop\AI全栈`）打开 PowerShell：

```powershell
# 1. 创建并激活虚拟环境（可选但推荐）
python -m venv .venv
.\.venv\Scripts\Activate

# 2. 安装后端依赖
pip install -r backend\requirements.txt

# 3. 启动后端 (方式 A: 直接运行)
cd backend
python main.py

# 或方式 B: 使用 uvicorn（带自动热重载，开发用）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动后，FastAPI 的默认文档可访问：

- OpenAPI 文档（Swagger UI）：http://localhost:8000/docs
- Redoc 文档：http://localhost:8000/redoc

---

## 打开前端页面

前端为静态 HTML 文件，可直接在浏览器打开：

- 在文件资源管理器中双击 `frontend\index.html` 打开
- 或者在 VS Code 中用 Live Server 插件打开，或右键 -> Open with Default Browser

前端默认请求地址为 `http://localhost:8000/translate`，因此请先确保后端已启动。

---

## 接口示例（curl）

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text":"人工智能正在改变我们的生活方式。"}'

# 可能的响应示例：
# {
#   "translation": "Artificial intelligence is changing the way we live.",
#   "keywords": ["Artificial intelligence","changing","lifestyle"]
# }
```

---

## 常见问题与排查

- 后端无法启动：端口 8000 被占用
  - 在 PowerShell 中查找占用该端口的进程：

```powershell
netstat -ano | Select-String ":8000"
```

  - 根据 PID 杀掉进程（谨慎操作）：

```powershell
taskkill /PID <PID> /F
```

- 前端无法连接后端：
  - 确认 `backend/main.py` 已启动且没有抛出异常。
  - 检查浏览器控制台（F12）是否有 CORS 或网络错误。
  - 后端示例中已允许所有来源（CORS allow_origins=["*"]），但生产环境请限制来源。

- 模型或 API 访问失败：
  - 检查 `backend/.env` 中的 `ALIYUN_API_KEY` 与 `ALIYUN_BASE_URL` 是否正确。
  - 如果使用公司内网或代理，确保 Python 的请求能通过代理访问外网。

---

## 安全与注意事项

- 当前示例直接在后端 `.env` 放置密钥，便于演示。实际部署请使用更安全的密钥管理方案（如环境变量注入、Vault、云服务密钥管理等）。
- 对外暴露接口时请加入鉴权（API Key / OAuth / JWT）与速率限制，避免滥用导致费用暴增。

---

## 开发者提示

- 更改模型或调用方式：请在 `backend/main.py` 中修改客户端调用逻辑与 prompt。
- 前端静态文件可替换为更复杂的 React/Vue 应用，但请保证请求地址与后端一致。

---

## 文件位置快速索引

- 后端主程序：`backend/main.py`
- 后端环境变量：`backend/.env`
- 前端页面：`frontend/index.html`

---

如需我把项目打包为可运行的 Docker 镜像、添加简单的 auth 层或把前端改为 React 项目，我可以继续帮你实现。