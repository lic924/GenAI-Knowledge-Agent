# 🤖 GenAI-Knowledge Agent

An interactive AI assistant that combines Retrieval-Augmented Generation (RAG), summarization, and writing style transformation.  
Built using **Ollama**, **LangChain**, **ChromaDB**, and **Streamlit**.

---

## 🚀 Features

- 📄 Document Upload (PDF/TXT)
- 🔍 Vector Search + Semantic Retrieval (ChromaDB + bge-m3 embeddings)
- 💬 Question Answering (powered by Qwen 2.5)
- ✍️ Rewrite mode (formal, casual, academic tone — coming soon)
- 📚 Automatic Document Summarization

---

## 🧠 Architecture
User → Streamlit UI
↓
File Upload
↓
Chunking → Embeddings (bge-m3)
↓
Chroma Vector DB
↓
RAG Retriever
↓
Qwen2.5-1.5B Response

---

## 🛠 Installation

### 1. Install Ollama
https://ollama.com/download

Then pull required models:

```bash
ollama pull qwen2.5:1.5b
ollama pull bge-m3

```
### 2. 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the app
```bash
streamlit run app.py
```
