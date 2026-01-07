# Translation - AI翻译助手

一个基于 FastAPI 和静态前端的 AI 翻译助手项目。

## 项目结构

```
Translation/
├── backend/              # FastAPI 后端
│   ├── main.py          # 主应用程序
│   └── __init__.py
├── frontend/            # 静态前端
│   └── index.html       # 前端页面
├── .github/
│   └── workflows/       # GitHub Actions 工作流
│       ├── ci.yml       # 后端 CI/CD
│       └── frontend-pages.yml  # 前端部署
├── Dockerfile           # Docker 镜像构建文件
├── requirements.txt     # Python 依赖
├── start.sh            # Linux/Mac 启动脚本
├── start.ps1           # Windows 启动脚本
└── README.md           # 项目文档
```

## 功能特性

- ✅ FastAPI 后端 API
- ✅ 现代化的静态前端界面
- ✅ Docker 容器化部署
- ✅ GitHub Actions CI/CD
- ✅ GitHub Pages 前端部署
- ✅ 跨平台启动脚本

## 快速开始

### 前置要求

- Python 3.10 或更高版本
- Docker (用于容器化部署)
- Git

### 本地开发

#### Linux/Mac

```bash
# 克隆仓库
git clone https://github.com/siwangchuan/Translation.git
cd Translation

# 设置环境变量
export ALIYUN_API_KEY='your-aliyun-api-key'

# 运行启动脚本
./start.sh
```

#### Windows

```powershell
# 克隆仓库
git clone https://github.com/siwangchuan/Translation.git
cd Translation

# 设置环境变量
$env:ALIYUN_API_KEY='your-aliyun-api-key'

# 运行启动脚本
.\start.ps1
```

后端服务将在 `http://localhost:8000` 启动。

### 访问前端

打开浏览器访问 `frontend/index.html` 或访问 GitHub Pages 部署的地址。

### API 文档

启动后端服务后，访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker 部署

### 构建镜像

```bash
docker build -t translation-backend .
```

### 运行容器

```bash
docker run -d \
  -p 8000:8000 \
  -e ALIYUN_API_KEY='your-aliyun-api-key' \
  --name translation-backend \
  translation-backend
```

### 使用 Docker Compose

项目已包含 `docker-compose.yml` 文件：

1. 复制环境变量示例：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件并设置你的 API Key

3. 启动服务：

```bash
docker-compose up -d
```

## CI/CD 部署

### 所需 Secrets

在 GitHub 仓库设置中配置以下 Secrets：

#### 1. GHCR_TOKEN (必需)

用于推送 Docker 镜像到 GitHub Container Registry。

**创建步骤：**
1. 访问 GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 设置权限：
   - ✅ `write:packages` - 上传容器到 GitHub Package Registry
   - ✅ `read:packages` - 下载容器从 GitHub Package Registry
   - ✅ `delete:packages` - 删除容器从 GitHub Package Registry
4. 生成 token 并复制
5. 在仓库 Settings > Secrets and variables > Actions > New repository secret
6. Name: `GHCR_TOKEN`, Value: 粘贴刚才复制的 token

#### 2. ALIYUN_API_KEY (必需)

用于调用阿里云翻译 API。

**设置步骤：**
1. 获取阿里云 API Key
2. 在仓库 Settings > Secrets and variables > Actions > New repository secret
3. Name: `ALIYUN_API_KEY`, Value: 你的阿里云 API Key

### GitHub Actions 工作流

#### 后端 CI/CD (`.github/workflows/ci.yml`)

触发条件：
- Push 到 `main` 或 `develop` 分支
- Pull Request 到 `main` 分支

流程：
1. **Lint and Test**: 安装依赖、运行代码检查和测试
2. **Build and Push**: 构建 Docker 镜像并推送到 GHCR

#### 前端部署 (`.github/workflows/frontend-pages.yml`)

触发条件：
- Push 到 `main` 分支且修改了 `frontend/` 目录
- 手动触发 (workflow_dispatch)

流程：
1. **Build**: 构建前端静态文件
2. **Deploy**: 部署到 GitHub Pages

### 启用 GitHub Pages

1. 进入仓库 Settings > Pages
2. Source: 选择 "GitHub Actions"
3. 保存设置

部署完成后，前端将在 `https://siwangchuan.github.io/Translation/` 访问。

## 从 GHCR 拉取镜像

```bash
# 登录 GHCR
echo $GHCR_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 拉取镜像
docker pull ghcr.io/siwangchuan/translation:latest

# 运行容器
docker run -d \
  -p 8000:8000 \
  -e ALIYUN_API_KEY='your-aliyun-api-key' \
  ghcr.io/siwangchuan/translation:latest
```

## API 端点

### GET /
健康检查，返回 API 状态信息。

### GET /health
服务健康状态检查。

### POST /translate
翻译文本接口。

**请求体：**
```json
{
  "text": "Hello, world!",
  "source_lang": "en",
  "target_lang": "zh"
}
```

**响应：**
```json
{
  "translated_text": "你好，世界！",
  "source_lang": "en",
  "target_lang": "zh"
}
```

## 开发

### 安装开发依赖

```bash
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black
```

### 代码格式化

```bash
black backend/
```

### 代码检查

```bash
flake8 backend/
```

### 运行测试

```bash
pytest tests/ -v
```

## 技术栈

- **后端**: FastAPI, Uvicorn, Pydantic
- **前端**: HTML5, CSS3, JavaScript (原生)
- **容器化**: Docker
- **CI/CD**: GitHub Actions
- **托管**: GitHub Container Registry, GitHub Pages

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
