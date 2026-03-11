# AI Video Prompt Compiler Service --- PRD

## 1. 專案概述

建立一個 AI Agent 驅動的影片生成服務。\
當系統接收到 API 請求後，透過 Agent SDK 進行語意理解與 Prompt 二次分析
(Prompt Refinement)，再呼叫外部影片生成 API 產生影片。

核心目標： - 將模糊的人類描述轉換為高品質影片生成提示詞 - 降低 Prompt
Engineering 門檻 - 提供統一的 AI 生成 API Gateway

------------------------------------------------------------------------

## 2. 目標用戶

  用戶類型        需求
  --------------- ----------------------
  AI 創作者       快速生成高品質影片
  SaaS 開發者     將影片生成整合到產品
  行銷人員        快速生成宣傳內容
  AI Agent 系統   作為影片生成中介服務

------------------------------------------------------------------------

## 3. 核心功能

### 3.1 Prompt 二次分析 (Prompt Refinement)

輸入：

"a cat drinking coffee in cyberpunk city"

Agent 分析後輸出：

A cinematic cyberpunk scene at night. Neon-lit futuristic city. An
orange cat sitting at a cafe table drinking coffee. Rain reflections on
the street. Shallow depth of field. Cinematic lighting.

功能：

-   語意補完
-   視覺元素補強
-   風格補充
-   鏡頭語言生成

------------------------------------------------------------------------

### 3.2 Prompt Compiler

將 Agent 分析結果轉換為影片模型最佳 Prompt 結構。

範例：

{ "scene": "cyberpunk city night", "subject": "orange cat drinking
coffee", "camera": "cinematic close-up", "style": "neon cyberpunk",
"lighting": "dramatic neon reflections" }

最終 Prompt：

"Cinematic cyberpunk city at night, neon reflections, orange cat
drinking coffee in cafe, rainy atmosphere, cinematic lighting"

------------------------------------------------------------------------

### 3.3 Video Generation

呼叫外部影片生成 API：

-   Runway
-   Pika
-   Kling
-   Sora (未來)

Example API:

POST /video/generate

{ "prompt": "...", "duration": 5, "aspect_ratio": "16:9" }

------------------------------------------------------------------------

### 3.4 任務管理 (Task System)

影片生成為非同步任務。

任務狀態：

-   queued
-   processing
-   completed
-   failed

查詢：

GET /tasks/{id}

------------------------------------------------------------------------

## 4. 系統架構

Client ↓ API Gateway ↓ Agent Layer (Prompt Refinement) ↓ Prompt Compiler
↓ Video Provider API ↓ Task Storage

------------------------------------------------------------------------

## 5. API 設計

### 5.1 Generate Video

POST /v1/video/generate

Request

{ "prompt": "cat drinking coffee in cyberpunk city", "duration": 5,
"ratio": "16:9" }

Response

{ "task_id": "task_abc123", "status": "queued" }

------------------------------------------------------------------------

### 5.2 Task Status

GET /v1/tasks/{task_id}

Response

{ "task_id": "task_abc123", "status": "completed", "video_url":
"https://cdn.example.com/video.mp4" }

------------------------------------------------------------------------

## 6. Agent 設計

Agent 任務：

1.  語意解析
2.  視覺補強
3.  Prompt 結構化

Prompt Template：

You are a professional prompt engineer for video generation.

Tasks: 1. Understand the user prompt 2. Expand it with cinematic visual
details 3. Improve scene description 4. Keep output concise

User Prompt: {prompt}

------------------------------------------------------------------------

## 7. 技術架構

  模組       技術
  ---------- ------------------
  API        FastAPI
  Agent      OpenAI Agent SDK
  Queue      Redis
  Worker     Celery / Arq
  Database   PostgreSQL
  Cache      Redis
  Storage    S3 Compatible

------------------------------------------------------------------------

## 8. 資料模型

  field             type
  ----------------- -----------
  id                uuid
  status            string
  original_prompt   text
  refined_prompt    text
  provider          string
  video_url         text
  created_at        timestamp

  : tasks

------------------------------------------------------------------------

## 9. 非功能需求

  項目     需求
  -------- ----------------------
  延遲     Agent 分析 \< 500ms
  擴展性   Worker 可水平擴展
  日誌     保存 Prompt Logs
  監控     Prometheus + Grafana

------------------------------------------------------------------------

## 10. 未來擴展

### Multi Provider

支援多影片模型：

-   Runway
-   Pika
-   Kling
-   Sora

系統可自動選擇最佳模型。

### Style Library

可指定風格：

-   cinematic
-   anime
-   documentary
-   pixar

### AI Director Agent

未來可生成完整分鏡：

User Prompt ↓ Director Agent ↓ Shot Planning ↓ Scene Generation ↓ Video
Stitching

------------------------------------------------------------------------

## 11. MVP 範圍

MVP 版本包含：

-   Prompt Refinement Agent
-   單一影片 API Provider
-   任務查詢 API
-   基本任務管理

------------------------------------------------------------------------

## 12. 成功指標

  指標             目標
  ---------------- ---------
  Prompt 改善率    \>30%
  影片生成成功率   \>95%
  平均生成時間     \<60 秒
