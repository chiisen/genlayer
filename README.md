# GenLayer

AI Video Prompt Compiler Service - 透過 AI Agent 將模糊的影片描述轉換為高品質提示詞，並呼叫 Kling API 生成影片。

## 功能

- **Prompt Refinement** - 使用 OpenAI Agent 將用戶模糊描述轉換為高品質影片提示詞
- **Prompt Compiler** - 將分析結果編譯為影片模型最佳格式
- **影片生成** - 整合 Kling API 進行影片生成
- **任務管理** - 基於 Redis 的非同步任務系統

## 技術棧

- **API**: FastAPI (Python 3.11+)
- **Agent**: OpenAI Agent SDK
- **Queue**: Redis
- **部署**: 本地 Python 環境

## 快速開始

### 前置需求

- Python 3.11+
- Redis

### 安裝

```bash
# 1. 複製環境變數
cp .env.example .env

# 2. 編輯 .env 填入 API Keys
# OPENAI_API_KEY=your_openai_api_key
# KLING_API_KEY=your_kling_api_key

# 3. 安裝依賴
pip install -e .

# 4. 啟動 Redis
brew services start redis

# 5. 啟動服務
uvicorn app.main:app --reload
```

### API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/health` | 健康檢查 |
| POST | `/v1/video/generate` | 建立影片生成任務 |
| GET | `/v1/tasks/{task_id}` | 查詢任務狀態 |

### 測試

```bash
# 單元測試
pytest tests/ -v

# Lint 檢查
ruff check app/
```

## 專案結構

```
genlayer/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── api/                 # API 路由
│   ├── agents/              # AI Agent
│   ├── services/            # 服務層
│   ├── schemas/             # Pydantic 模型
│   └── core/                # 核心配置
├── tests/                   # 測試
├── pyproject.toml           # 專案配置
└── .env.example            # 環境變數範本
```

## License

MIT
