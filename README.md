# AI 翻译助手 — 快速启动说明

这是一个示例项目，包含：
- 后端：FastAPI（`backend/main.py`），提供 `/translate` 接口。
- 前端：静态页面（`frontend/index.html`），通过浏览器调用后端接口显示翻译结果。

快速目标：在本机启动后端并通过浏览器访问示例页面。

## 最快启动（开发机器）
1. 安装依赖：

```powershell
cd C:\Users\si\Desktop\AI全栈
pip install -r backend\requirements.txt
```

2. 在 `backend/.env` 中设置（必须）：

```
ALIYUN_API_KEY=你的_api_key
ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

3. 启动后端：

```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. 在浏览器打开（推荐）：

- 后端 API 文档（验证后端是否可用）： http://localhost:8000/docs
- 若后端托管了前端：直接访问 http://localhost:8000/ （会返回 `frontend/index.html`）

或直接打开 `frontend\index.html`（file://）——页面会自动尝试连接 `http://localhost:8000`。

## 使用 ngrok 暴露到公网（临时）

在另一终端运行：

```powershell
ngrok http 8000
```

复制 ngrok 给您的 `https://...` 地址，外部设备即可访问该地址并使用翻译服务。

## 接口示例（curl）

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text":"人工智能正在改变我们的生活方式。"}'
```

示例返回：
```json
{
  "translation": "Artificial intelligence is changing the way we live.",
  "keywords": ["Artificial intelligence","changing","lifestyle"]
}
```

## 常见问题快速排查
- 无法连接：确认后端在端口 `8000` 运行。命令：

```powershell
netstat -ano | Select-String ":8000"
```

- 端口被占用：根据 PID 强制结束进程（谨慎）：

```powershell
taskkill /PID <PID> /F
```

- 模型调用超时或失败：检查 `backend` 终端输出与 `.env` 中的 API Key 是否正确。

## 文件索引
- 后端： `backend/main.py`
- 环境变量： `backend/.env`
- 前端： `frontend/index.html`

如需，我可以后续：生成 `Dockerfile`、添加 GitHub Actions CI/CD 或将前端部署到 GitHub Pages。
