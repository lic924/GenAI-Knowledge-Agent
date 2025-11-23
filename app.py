import streamlit as st
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ========== 設定頁面 ==========
st.set_page_config(page_title="GenAI Knowledge Agent", page_icon="🤖")
st.title("🤖 GenAI Knowledge Agent")
st.subheader("RAG + Summarization + Style Rewrite")

# ========== 初始化模型（只在第一次載入時做） ==========
@st.cache_resource
def load_models():
    # 嵌入模型，用於 RAG 檢索
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # 小型生成模型（英文較強，但也能處理一些中文）
    gen_pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )
    return embedder, gen_pipe

embedder, gen_pipe = load_models()

# ========== Session State ==========
if "chunks" not in st.session_state:
    st.session_state["chunks"] = []
if "embeddings" not in st.session_state:
    st.session_state["embeddings"] = None
if "full_text" not in st.session_state:
    st.session_state["full_text"] = ""

# ========== 工具函式 ==========
def load_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        return file.read().decode("utf-8")

def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def build_index(text):
    chunks = chunk_text(text)
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    st.session_state["chunks"] = chunks
    st.session_state["embeddings"] = embeddings

def retrieve_context(query, k=3):
    if st.session_state["embeddings"] is None:
        return ""
    q_emb = embedder.encode([query], convert_to_numpy=True)[0]
    emb = st.session_state["embeddings"]

    # cosine similarity
    dot = emb @ q_emb
    norm_emb = np.linalg.norm(emb, axis=1)
    norm_q = np.linalg.norm(q_emb)
    scores = dot / (norm_emb * norm_q + 1e-10)

    top_idx = np.argsort(scores)[::-1][:k]
    selected = [st.session_state["chunks"][i] for i in top_idx]
    return "\n\n".join(selected)

def generate(text, max_new_tokens=256):
    # 用 flan-t5-small 做 text2text generation
    out = gen_pipe(
        text,
        max_new_tokens=max_new_tokens,
        do_sample=False
    )
    return out[0]["generated_text"].strip()

# ========== 檔案上傳 ==========
uploaded_file = st.file_uploader("📁 上傳 PDF 或 TXT 文件", type=["pdf", "txt"])

if uploaded_file:
    st.success("文件已上傳，正在建立索引（首次可能較慢）...")
    full_text = load_text(uploaded_file)
    st.session_state["full_text"] = full_text
    build_index(full_text)
    st.info(f"文件長度：約 {len(full_text)} 字元，chunk 數量：{len(st.session_state['chunks'])}")
else:
    full_text = st.session_state["full_text"]

# ========== 模式選單 ==========
modes = ["📌 問答模式（RAG）", "📝 摘要模式", "✍️ 文風改寫模式"]
selected_mode = st.radio("選擇功能模式：", modes)

user_input = st.text_input("輸入問題 / 要改寫的文字：")

tone = None
if selected_mode == "✍️ 文風改寫模式":
    tone = st.selectbox(
        "選擇文風：",
        ["正式", "學術", "口語", "簡潔摘要", "可愛風"]
    )

# ========== 執行按鈕 ==========
if st.button("🚀 執行任務"):

    # 1) 問答模式（RAG）
    if selected_mode.startswith("📌"):
        if not uploaded_file and not st.session_state["chunks"]:
            st.error("請先上傳文件！")
        elif not user_input:
            st.error("請輸入問題。")
        else:
            context = retrieve_context(user_input, k=3)
            prompt = (
                "你是一個文件助理，請根據下列內容回答問題，"
                "盡量使用繁體中文回答，並簡短扼要。\n\n"
                f"[文件內容]\n{context}\n\n"
                f"[問題]\n{user_input}\n\n"
                "回答："
            )
            answer = generate(prompt, max_new_tokens=256)
            st.markdown("### 🧠 回答")
            st.write(answer)

    # 2) 摘要模式
    elif selected_mode.startswith("📝"):
        if not full_text:
            st.error("請先上傳文件！")
        else:
            prompt = (
                "請將以下文字重點式總結，使用繁體中文，條列 5~8 點：\n\n"
                f"{full_text[:6000]}"
            )
            summary = generate(prompt, max_new_tokens=256)
            st.markdown("### 📝 摘要結果")
            st.write(summary)

    # 3) 文風改寫模式
    elif selected_mode.startswith("✍️"):
        if not user_input:
            st.error("請先輸入要改寫的文字。")
        else:
            prompt = (
                f"請將以下文字改寫成「{tone}」風格，"
                "並使用繁體中文輸出：\n\n"
                f"{user_input}"
            )
            rewritten = generate(prompt, max_new_tokens=256)
            st.markdown("### ✍️ 改寫結果")
            st.write(rewritten)