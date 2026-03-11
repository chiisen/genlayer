# AI Video Prompt Compiler Service - 工作計劃

## TL;DR

> **快速摘要**：建立 AI Agent 驅動的影片生成服務，透過 Prompt Refinement 將用戶模糊描述轉換為高品質影片提示詞，再呼叫 Kling API 生成影片。

> **交付物**：
> - FastAPI 服務 (`app/`)
> - Prompt Refinement Agent 模組
> - Kling API 整合
> - 任務管理系統 (Redis 儲存)
> - API 文件

> **預估工作量**：Medium
> **平行執行**：YES - 多 waves
> **關鍵路徑**：專案結構 → 核心模組 → API → 整合測試

---

## Context

### 原始需求 (PRD.md)
- Prompt Refinement Agent 將模糊描述轉為高品質提示詞
- Prompt Compiler 編譯為影片模型最佳格式
- 呼叫外部影片生成 API (Kling)
- 非同步任務管理

### 訪談摘要
**討論重點**：
- Provider 選擇：**Kling** (性價比高)
- 基礎設施：**僅使用 Redis** (任務資料不持久化)
- 部署方式：本地 Python 環境
- 測試策略：pytest

### 架構調整 (相較 PRD)
- **移除 PostgreSQL**：改用 Redis 儲存任務狀態
- **簡化 Worker**：使用同步處理或 asyncio 即可，MVP 階段不需要 Celery

---

## Work Objectives

### 核心目標
建立 MVP 版本的 AI Video Prompt Compiler Service，實現：
1. 接收用戶影片生成請求
2. 透過 Agent SDK 進行 Prompt Refinement
3. 呼叫 Kling API 生成影片
4. 透過 Redis 管理任務狀態

### 具體交付物
- `app/main.py` - FastAPI 應用入口
- `app/api/v1/video.py` - POST /v1/video/generate 端點
- `app/api/v1/tasks.py` - GET /v1/tasks/{task_id} 端點
- `app/agents/prompt_refiner.py` - Prompt Refinement Agent
- `app/services/kling.py` - Kling API 整合
- `app/services/redis_task.py` - 任務狀態管理 (Redis)
- `app/schemas/` - Pydantic 模型
- `tests/` - pytest 測試
- `pyproject.toml` - 專案配置

### 完成定義
- [ ] `python -m uvicorn app.main:app` 可啟動服務
- [ ] POST /v1/video/generate 回傳 task_id
- [ ] GET /v1/tasks/{task_id} 可查詢任務狀態
- [ ] Agent 正確執行 Prompt Refinement
- [ ] pytest 測試通過

### Must Have
- [ ] FastAPI 服務可正常啟動
- [ ] 兩支 API 端點正常運作
- [ ] Prompt Refinement 功能正常
- [ ] Kling API 整合正常
- [ ] 任務狀態管理正常

### Must NOT Have (Guardrails)
- [ ] **不使用 PostgreSQL** - 僅用 Redis 儲存任務
- [ ] **不實作 Multi-Provider** - MVP 僅 Kling
- [ ] **不實作 Style Library** - 未來功能
- [ ] **不實作 AI Director Agent** - 未來功能

---

## Verification Strategy

### 測試決策
- **基礎設施存在**：YES (pytest)
- **自動化測試**：YES (pytest)
- **框架**：pytest + pytest-asyncio

### QA 政策
每個任務必須包含 agent-executed QA scenarios。
- **API 測試**：使用 FastAPI TestClient + pytest
- **Agent 測試**：Mock OpenAI API
- **整合測試**：使用 Docker Redis 或 fakeredis

---

## Execution Strategy

### 平行執行 Waves

```
Wave 1 (立即開始 - 基礎設施):
├── T1: 建立專案結構 + pyproject.toml [quick]
├── T2: 建立 FastAPI 入口 + CORS 設定 [quick]
├── T3: 建立 Pydantic Schemas [quick]
├── T4: Redis 連接配置 + 任務服務 [quick]
└── T5: 設定日誌 + 環境變數 [quick]

Wave 2 (After Wave 1 - 核心模組):
├── T6: Prompt Refiner Agent 實作 [deep]
├── T7: Kling API 客戶端 [deep]
├── T8: Prompt Compiler 工具 [quick]
└── T9: 任務狀態管理 (Redis) [deep]

Wave 3 (After Wave 2 - API 層):
├── T10: POST /v1/video/generate 端點 [deep]
├── T11: GET /v1/tasks/{task_id} 端點 [deep]
└── T12: Error Handler + 中間件 [quick]

Wave 4 (After Wave 3 - 測試):
├── T13: API 單元測試 [deep]
├── T14: Agent 單元測試 [deep]
├── T15: 整合測試 [deep]
└── T16: 程式碼品質檢查 (pylint/black) [quick]

Wave FINAL (After ALL - 獨立審查):
├── F1: Plan Compliance Audit (oracle)
├── F2: Code Quality Review (unspecified-high)
├── F3: Real Manual QA (unspecified-high)
└── F4: Scope Fidelity Check (deep)
```

### 依賴矩陣
- T1-T5: — — 6-9
- T6-T9: 1-5 — 10-12
- T10-T12: 6-9 — 13-16
- T13-T16: 10-12 — F1-F4

---

## TODOs

### Wave 1: 基礎設施

- [ ] 1. 建立專案結構 + pyproject.toml

  **What to do**:
  - 建立 `app/` 目錄結構
  - 建立 `app/__init__.py`, `app/api/`, `app/agents/`, `app/services/`, `app/schemas/`
  - 建立 `pyproject.toml` 含 FastAPI, openai, redis, pydantic, pytest 等依賴
  - 建立 `.env.example` 環境變數範本

  **Must NOT do**:
  - 不要建立 Django 或其他框架結構

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T2-T5)
  - **Blocks**: T6-T9
  - **Blocked By**: None

  **References**:
  - FastAPI 官方文檔: 建立專案結構範例

  **Acceptance Criteria**:
  - [ ] 目錄結構建立完成
  - [ ] pyproject.toml 包含所有必要依賴
  - [ ] `python -m pip install -e .` 安裝成功

  **QA Scenarios**:
  ```
  Scenario: 專案結構正確建立
    Tool: Bash
    Preconditions: 無
    Steps:
      1. ls -la app/ 確認目錄存在
      2. python -m pip install -e . 確認安裝成功
    Expected Result: 目錄存在且安裝成功
    Evidence: .sisyphus/evidence/task-1-structure.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 建立專案結構 + pyproject.toml`
  - Files: `pyproject.toml`, `app/`

- [ ] 2. 建立 FastAPI 入口 + CORS 設定

  **What to do**:
  - 建立 `app/main.py`
  - 設定 FastAPI app 實例
  - 設定 CORS 中間件
  - 包含基本 health check 端點

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T3-T5)
  - **Blocks**: T10-T12
  - **Blocked By**: None

  **References**:
  - FastAPI 官方文檔: CORS 設定

  **Acceptance Criteria**:
  - [ ] FastAPI app 可正常啟動
  - [ ] GET /health 端點正常回應
  - [ ] CORS 設定正確

  **QA Scenarios**:
  ```
  Scenario: FastAPI 服務正常啟動
    Tool: Bash
    Preconditions: pyproject.toml 已安裝
    Steps:
      1. timeout 5 python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
      2. sleep 2
      3. curl http://localhost:8000/health
    Expected Result: {"status":"ok"}
    Evidence: .sisyphus/evidence/task-2-health.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 建立 FastAPI 入口 + CORS`
  - Files: `app/main.py`

- [ ] 3. 建立 Pydantic Schemas

  **What to do**:
  - 建立 `app/schemas/video.py` - 影片生成請求/回應
  - 建立 `app/schemas/task.py` - 任務狀態模型
  - 包含 Request/Response DTO

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1, T2, T4-T5)
  - **Blocks**: T10-T11
  - **Blocked By**: None

  **References**:
  - FastAPI 官方文檔: Pydantic 模型

  **Acceptance Criteria**:
  - [ ] Schema 類別正確建立
  - [ ] Request validation 正常運作

  **QA Scenarios**:
  ```
  Scenario: Pydantic Schema 正確驗證
    Tool: Bash (pytest)
    Preconditions: pytest 已安裝
    Steps:
      1. python -c "from app.schemas.video import VideoGenerateRequest; r = VideoGenerateRequest(prompt='test', duration=5, ratio='16:9'); print(r.model_dump())"
    Expected Result: 正確輸出 JSON
    Evidence: .sisyphus/evidence/task-3-schema.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 建立 Pydantic Schemas`
  - Files: `app/schemas/`

- [ ] 4. Redis 連接配置 + 任務服務

  **What to do**:
  - 建立 `app/core/config.py` - 環境變數管理
  - 建立 `app/core/redis.py` - Redis 連接
  - 建立 `app/services/redis_task.py` - 任務 CRUD 操作
  - 定義任務狀態 enum (queued, processing, completed, failed)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1-T3, T5)
  - **Blocks**: T9
  - **Blocked By**: None

  **References**:
  - Redis 官方文檔: Python redis 客戶端

  **Acceptance Criteria**:
  - [ ] Redis 連接可建立
  - [ ] 任務服務基本操作正常

  **QA Scenarios**:
  ```
  Scenario: Redis 連接正常
    Tool: Bash
    Preconditions: Redis 服務運行中
    Steps:
      1. python -c "from app.core.redis import get_redis; r = get_redis(); print(r.ping())"
    Expected Result: True
    Evidence: .sisyphus/evidence/task-4-redis.{ext}
  ```

  **Commit**: YES
  - Message: `feat: Redis 連接配置 + 任務服務`
  - Files: `app/core/`, `app/services/redis_task.py`

- [ ] 5. 設定日誌 + 環境變數

  **What to do**:
  - 建立 `app/core/logging.py` - 日誌配置
  - 建立 `.env.example` 範本
  - 設定結構化日誌格式

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1-T4)
  - **Blocks**: All tasks
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] 日誌正確輸出到 stdout
  - [ ] .env.example 包含所有必要變數

  **QA Scenarios**:
  ```
  Scenario: 日誌配置正確
    Tool: Bash
    Preconditions: 無
    Steps:
      1. python -c "from app.core.logging import setup_logging; setup_logging(); import logging; logging.info('test')"
    Expected Result: 日誌正確輸出
    Evidence: .sisyphus/evidence/task-5-logging.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 設定日誌 + 環境變數`
  - Files: `app/core/logging.py`, `.env.example`

---

### Wave 2: 核心模組

- [ ] 6. Prompt Refiner Agent 實作

  **What to do**:
  - 建立 `app/agents/prompt_refiner.py`
  - 實作 Agent 類別，使用 OpenAI Agent SDK
  - 實現語意解析、視覺補強、Prompt 結構化
  - 設計 Agent Prompt Template

  **Must NOT do**:
  - 不要 hardcode API key

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T7-T9)
  - **Blocks**: T10
  - **Blocked By**: T1-T5

  **References**:
  - OpenAI Agent SDK 文檔
  - PRD.md: Agent Prompt Template 章節

  **Acceptance Criteria**:
  - [ ] Agent 可接收原始 prompt
  - [ ] 回傳結構化的 refined prompt
  - [ ] 錯誤處理正常

  **QA Scenarios**:
  ```
  Scenario: Agent 正確執行 Prompt Refinement
    Tool: Bash (pytest with mock)
    Preconditions: OPENAI_API_KEY 已設定
    Steps:
      1. python -c "from app.agents.prompt_refiner import PromptRefiner; p = PromptRefiner(); result = p.refine('a cat drinking coffee in cyberpunk city'); print(result)"
    Expected Result: 回傳結構化的高品質 prompt
    Evidence: .sisyphus/evidence/task-6-agent.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 Prompt Refiner Agent`
  - Files: `app/agents/prompt_refiner.py`

- [ ] 7. Kling API 客戶端

  **What to do**:
  - 建立 `app/services/kling.py`
  - 實作 Kling API 客戶端
  - 處理影片生成請求
  - 處理回應並提取 video_url

  **Must NOT do**:
  - 不要上傳真實 API key 到版本控制

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T6, T8-T9)
  - **Blocks**: T10
  - **Blocked By**: T1-T5

  **References**:
  - Kling API 文檔 (官方)

  **Acceptance Criteria**:
  - [ ] 客戶端可發送請求到 Kling API
  - [ ] 回應正確解析

  **QA Scenarios**:
  ```
  Scenario: Kling 客戶端正確配置
    Tool: Bash (pytest with mock)
    Preconditions: KLING_API_KEY 已設定
    Steps:
      1. python -c "from app.services.kling import KlingClient; print(KlingClient.__name__)"
    Expected Result: 類別正確匯入
    Evidence: .sisyphus/evidence/task-7-kling.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 Kling API 客戶端`
  - Files: `app/services/kling.py`

- [ ] 8. Prompt Compiler 工具

  **What to do**:
  - 建立 `app/services/prompt_compiler.py`
  - 將 Agent 輸出編譯為最終影片 Prompt
  - 組合 scene, subject, camera, style, lighting

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T6-T7, T9)
  - **Blocks**: T10
  - **Blocked By**: T1-T5

  **References**:
  - PRD.md: Prompt Compiler 章節

  **Acceptance Criteria**:
  - [ ] 正確編譯各元素為最終 Prompt
  - [ ] 測試案例通過

  **QA Scenarios**:
  ```
  Scenario: Prompt Compiler 正確編譯
    Tool: Bash (pytest)
    Preconditions: 無
    Steps:
      1. python -c "from app.services.prompt_compiler import compile_prompt; result = compile_prompt({'scene': 'cyberpunk city', 'subject': 'cat', 'camera': 'close-up'}); print(result)"
    Expected Result: 正確輸出編譯後的 prompt
    Evidence: .sisyphus/evidence/task-8-compiler.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 Prompt Compiler`
  - Files: `app/services/prompt_compiler.py`

- [ ] 9. 任務狀態管理 (Redis)

  **What to do**:
  - 擴展 `app/services/redis_task.py`
  - 實作完整的任務狀態管理
  - 實現 create_task, get_task, update_task 方法
  - 設定 TTL 過期策略

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T6-T8)
  - **Blocks**: T10-T11
  - **Blocked By**: T4

  **References**:
  - Redis 官方文檔: TTL 操作

  **Acceptance Criteria**:
  - [ ] 任務可正確建立、查詢、更新
  - [ ] TTL 正確設定

  **QA Scenarios**:
  ```
  Scenario: 任務狀態管理正確
    Tool: Bash (pytest with fakeredis)
    Preconditions: fakeredis 已安裝
    Steps:
      1. python -c "from app.services.redis_task import TaskService; print(TaskService.__name__)"
    Expected Result: 正確匯入
    Evidence: .sisyphus/evidence/task-9-task.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作任務狀態管理 (Redis)`
  - Files: `app/services/redis_task.py`

---

### Wave 3: API 層

- [ ] 10. POST /v1/video/generate 端點

  **What to do**:
  - 建立 `app/api/v1/video.py`
  - 實作影片生成端點
  - 整合 Agent + Compiler + Kling + Task Service
  - 處理非同步任務派發

  **Must NOT do**:
  - 不要在請求處理中直接等待影片生成完成

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T11-T12)
  - **Blocks**: T13-T15
  - **Blocked By**: T6-T9

  **References**:
  - PRD.md: API 設計章節

  **Acceptance Criteria**:
  - [ ] 端點正確處理請求
  - [ ] 回傳 task_id 和 status: queued

  **QA Scenarios**:
  ```
  Scenario: POST /v1/video/generate 正確處理
    Tool: Bash (FastAPI TestClient)
    Preconditions: FastAPI app 已設定
    Steps:
      1. python -c "from fastapi.testclient import TestClient; from app.main import app; c = TestClient(app); r = c.post('/v1/video/generate', json={'prompt': 'cat', 'duration': 5, 'ratio': '16:9'}); print(r.json())"
    Expected Result: {"task_id": "...", "status": "queued"}
    Evidence: .sisyphus/evidence/task-10-generate.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 POST /v1/video/generate 端點`
  - Files: `app/api/v1/video.py`

- [ ] 11. GET /v1/tasks/{task_id} 端點

  **What to do**:
  - 建立 `app/api/v1/tasks.py`
  - 實作任務查詢端點
  - 從 Redis 讀取任務狀態
  - 回傳完整任務資訊

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T10, T12)
  - **Blocks**: T13-T15
  - **Blocked By**: T9

  **References**:
  - PRD.md: API 設計章節

  **Acceptance Criteria**:
  - [ ] 端點正確回傳任務狀態
  - [ ] 404 處理正確

  **QA Scenarios**:
  ```
  Scenario: GET /v1/tasks/{task_id} 正確處理
    Tool: Bash (FastAPI TestClient)
    Preconditions: FastAPI app 已設定
    Steps:
      1. python -c "from fastapi.testclient import TestClient; from app.main import app; c = TestClient(app); r = c.get('/v1/tasks/nonexistent'); print(r.status_code)"
    Expected Result: 404
    Evidence: .sisyphus/evidence/task-11-task.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 GET /v1/tasks/{task_id} 端點`
  - Files: `app/api/v1/tasks.py`

- [ ] 12. Error Handler + 中間件

  **What to do**:
  - 建立 `app/api/errors.py` - 自訂錯誤類別
  - 建立 `app/middleware/` - 自訂中間件
  - 實作全域錯誤處理
  - 設定 request ID 中間件

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with T10-T11)
  - **Blocks**: All
  - **Blocked By**: T2

  **References**:
  - FastAPI 官方文檔: Error handling

  **Acceptance Criteria**:
  - [ ] 錯誤正確回傳標準格式

  **QA Scenarios**:
  ```
  Scenario: 錯誤處理正確
    Tool: Bash
    Preconditions: 無
    Steps:
      1. curl http://localhost:8000/nonexistent
    Expected Result: 404 或適當錯誤回應
    Evidence: .sisyphus/evidence/task-12-error.{ext}
  ```

  **Commit**: YES
  - Message: `feat: 實作 Error Handler + 中間件`
  - Files: `app/api/errors.py`, `app/middleware/`

---

### Wave 4: 測試

- [ ] 13. API 單元測試

  **What to do**:
  - 建立 `tests/test_api/` 目錄
  - 測試 video 端點
  - 測試 tasks 端點
  - 使用 TestClient + fakeredis

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T14-T16)
  - **Blocks**: F1-F4
  - **Blocked By**: T10-T12

  **References**:
  - FastAPI 測試文檔

  **Acceptance Criteria**:
  - [ ] 所有 API 測試通過

  **QA Scenarios**:
  ```
  Scenario: API 單元測試通過
    Tool: Bash
    Preconditions: pytest 已安裝
    Steps:
      1. pytest tests/test_api/ -v
    Expected Result: 所有測試通過
    Evidence: .sisyphus/evidence/task-13-api-test.{ext}
  ```

  **Commit**: YES
  - Message: `test: API 單元測試`
  - Files: `tests/test_api/`

- [ ] 14. Agent 單元測試

  **What to do**:
  - 建立 `tests/test_agents/` 目錄
  - 測試 Prompt Refiner Agent
  - 使用 unittest.mock Mock OpenAI API

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T13, T15-T16)
  - **Blocks**: F1-F4
  - **Blocked By**: T6

  **Acceptance Criteria**:
  - [ ] 所有 Agent 測試通過

  **QA Scenarios**:
  ```
  Scenario: Agent 單元測試通過
    Tool: Bash
    Preconditions: pytest 已安裝
    Steps:
      1. pytest tests/test_agents/ -v
    Expected Result: 所有測試通過
    Evidence: .sisyphus/evidence/task-14-agent-test.{ext}
  ```

  **Commit**: YES
  - Message: `test: Agent 單元測試`
  - Files: `tests/test_agents/`

- [ ] 15. 整合測試

  **What to do**:
  - 建立 `tests/test_integration/` 目錄
  - 測試完整流程 (從請求到任務建立)
  - 使用 fakeredis 模擬 Redis

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T13-T14, T16)
  - **Blocks**: F1-F4
  - **Blocked By**: T10-T12

  **Acceptance Criteria**:
  - [ ] 整合測試通過

  **QA Scenarios**:
  ```
  Scenario: 整合測試通過
    Tool: Bash
    Preconditions: pytest + fakeredis 已安裝
    Steps:
      1. pytest tests/test_integration/ -v
    Expected Result: 所有測試通過
    Evidence: .sisyphus/evidence/task-15-integration-test.{ext}
  ```

  **Commit**: YES
  - Message: `test: 整合測試`
  - Files: `tests/test_integration/`

- [ ] 16. 程式碼品質檢查

  **What to do**:
  - 設定 pylint 或 ruff
  - 設定 black 格式化
  - 執行檢查並修復問題

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with T13-T15)
  - **Blocks**: F1-F4
  - **Blocked By**: All

  **Acceptance Criteria**:
  - [ ] pylint/black 檢查通過

  **QA Scenarios**:
  ```
  Scenario: 程式碼品質檢查通過
    Tool: Bash
    Preconditions: pylint/black 已安裝
    Steps:
      1. ruff check app/
      2. ruff format --check app/
    Expected Result: 無錯誤/警告
    Evidence: .sisyphus/evidence/task-16-lint.{ext}
  ```

  **Commit**: YES
  - Message: `chore: 程式碼品質檢查`
  - Files: 配置文件

---

### Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search codebase for forbidden patterns. Check evidence files exist.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run linter + formatter. Review all files for: style issues, unused imports, hardcoded secrets.
  Output: `Lint [PASS/FAIL] | Format [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Detect cross-task contamination.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | VERDICT`

---

## Commit Strategy

- **1**: `feat: 建立專案結構 + pyproject.toml`
- **2**: `feat: 建立 FastAPI 入口 + CORS`
- **3**: `feat: 建立 Pydantic Schemas`
- **4**: `feat: Redis 連接配置 + 任務服務`
- **5**: `feat: 設定日誌 + 環境變數`
- **6**: `feat: 實作 Prompt Refiner Agent`
- **7**: `feat: 實作 Kling API 客戶端`
- **8**: `feat: 實作 Prompt Compiler`
- **9**: `feat: 實作任務狀態管理 (Redis)`
- **10**: `feat: 實作 POST /v1/video/generate 端點`
- **11**: `feat: 實作 GET /v1/tasks/{task_id} 端點`
- **12**: `feat: 實作 Error Handler + 中間件`
- **13**: `test: API 單元測試`
- **14**: `test: Agent 單元測試`
- **15**: `test: 整合測試`
- **16**: `chore: 程式碼品質檢查`

---

## Success Criteria

### 驗證命令
```bash
# 啟動服務
python -m uvicorn app.main:app --reload

# 測試端點
curl -X POST http://localhost:8000/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "cat drinking coffee in cyberpunk city", "duration": 5, "ratio": "16:9"}'

# 執行測試
pytest tests/ -v
```

### 最終檢查清單
- [ ] 所有 "Must Have" 已實現
- [ ] 所有 "Must NOT Have" 已排除
- [ ] 所有測試通過
- [ ] API 文件正確生成 (FastAPI auto-doc)
