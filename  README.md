# 🤖 GenAI Knowledge Agent  
*A Lightweight RAG + Summarization + Style-Rewrite AI Assistant (No API Keys Required)*

---

## 📌 中文摘要（約 300 字）

本專題實作一個名為 **「GenAI Knowledge Agent」** 的智慧型文件助理系統，整合文件問答（RAG）、自動摘要生成與文風改寫等多項自然語言處理能力。系統使用者可透過網頁介面上傳 PDF 或 TXT 檔案，系統會將文件分段並使用 Sentence-Transformers 模型產生語意向量，作為後續查詢與語意檢索之基礎。

若使用者提出問題，系統會依照語意相似度挑選文件中最相關的內容，並交由 HuggingFace 上的開源生成式模型進行回覆，形成 Retrieval-Augmented Generation 工作流程。此外，本系統亦提供自動摘要與多種文風改寫功能，包括正式、口語、學術、簡潔與可愛風格等，以支援不同場合與應用需求。

本系統基於 CPU 即可執行，不需使用 OpenAI API，也不需額外安裝 Ollama，因此可成功部署於 Streamlit Cloud。本專題展示開源模型與輕量架構整合之可行性，證明低成本條件仍可建構具實用性與擴展性的 AI 文件助理。

---

## 🇬🇧 English Abstract

This project presents **GenAI Knowledge Agent**, a lightweight intelligent document assistant that integrates Retrieval-Augmented Generation (RAG), text summarization, and writing-style transformation. Users can upload PDF or text files through a Streamlit-based web interface. The system automatically chunks the input document and generates semantic embeddings using the Sentence-Transformers model for similarity-based retrieval.

When a query is submitted, the system retrieves the most relevant text segments and forwards them to an open-source HuggingFace model for grounded response generation. The system also supports automatic summarization and style rewriting features, including formal, academic, conversational, concise, and playful writing tones.

A key design goal is full **API-free and server-local execution**, enabling deployment to Streamlit Cloud without requiring paid model keys or local inference servers such as Ollama. This demonstrates a practical, low-cost approach to building an extensible, open-source document-aware AI assistant.

---

## 🧠 System Features

| 功能 | 說明 |
|------|------|
| 📌 RAG 文件問答 | 從上傳文件中檢索語意相關內容並回答問題 |
| 📝 自動摘要 | 將長文本壓縮成條列式摘要 |
| ✍️ 文風改寫 | 依照風格進行內容改寫（正式/口語/學術/可愛等） |
| 🚫 無需 API Key | 採用 HuggingFace 開源模型完全不用 OpenAI |

---

## 🏗️ System Architecture
       ┌───────── User ─────────┐
                      │
                      ▼
            📁 Upload PDF/TXT
                      │
                      ▼
 ┌──────────────── Chunk & Embed ────────────────┐
 │   SentenceTransformer (MiniLM-L6-v2)           │
 └───────────────────────┬────────────────────────┘
                         │
                         ▼
          🔍 Cosine Similarity Retrieval
                         │
                         ▼
 ┌──────── HuggingFace text2text Model ────────┐
 │  (flan-t5-small)                             │
 └───────────────────┬─────────────────────────┘
                     │
                     ▼
          💬 Final Answer / Summary / Rewrite
---

---

點擊 `Deploy`，等待首次模型自動下載

> ⚠️ 📌 *第一次啟動可能需要 1–3 分鐘（模型下載），之後會快很多。*

---

## 📚 Demo 使用方式

系統提供三種核心模式：

| 模式 | 功能描述 |
|------|----------|
| 📌 RAG 問答 | 根據上傳文件內容回答問題 |
| 📝 摘要生成 | 將長文件摘要為條列式重點 |
| ✍️ 文風改寫 | 將使用者輸入文字改寫成指定語氣 |

使用方式：

1. 上傳 PDF/TXT 文件  
2. 選擇所需功能模式  
3. 輸入問題或文字  
4. 點擊 🚀「執行任務」  
5. 查看模型輸出結果  

---

## 📓 Agent 開發過程對話紀錄

依課程要求，本專案包含 AI 協同開發紀錄，可用於回溯設計決策、錯誤排查與模型選型過程。

紀錄內容包含：

- 問題定義與需求分析  
- 架構設計（Ollama → HuggingFace 遷移決策）  
- 環境與部署 Debug 記錄  
- 功能調整與介面迭代  
- 最終部署與收尾

完整紀錄已整理為附件：

📁 `Agent_Development_Log.pdf`（或 `Agent_Development_Log.md`）

> 若需審查教學用，可加入報告附錄；若作業未要求，可存於 Repo 內即可。

---

## 🔮 Future Improvement

- 支援多文件索引（Multi-Document RAG）
- 本地端模型切換（Ollama / WebGPU / HuggingFace Quantized）
- 支援中文更強模型，例如：Qwen 精簡版離線推論
- UI 增加歷史記錄、多結果比較、PDF 頁面定位等功能

---

## 📜 License

MIT License © 2025

---