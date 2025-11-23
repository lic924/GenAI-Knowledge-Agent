import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from pypdf import PdfReader

# Models
llm = Ollama(model="qwen2.5:1.5b", base_url="http://localhost:11434")
embed_model = OllamaEmbeddings(model="bge-m3", base_url="http://localhost:11434")

st.set_page_config(page_title="GenAI Knowledge Agent", page_icon="🤖")
st.title("🤖 GenAI Knowledge Agent")
st.subheader("RAG + Summarization + Writing Style Transformer")

uploaded_file = st.file_uploader("📁 上傳 PDF 或 TXT 文件", type=["pdf", "txt"])

db = None
text = ""

if uploaded_file:
    st.success("文件已上傳，正在處理...")

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages])
    else:
        text = uploaded_file.read().decode("utf-8")

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_text(text)

    db = Chroma.from_texts(chunks, embed_model)

modes = ["📌 問答模式", "📝 摘要模式", "✍️ 文風改寫模式"]

selected_mode = st.radio("選擇功能模式：", modes)

user_input = st.text_input("輸入文字或問題：")

# 声調選擇器 (rewrite mode)
tone = None
if selected_mode == "✍️ 文風改寫模式":
    tone = st.selectbox(
        "選擇文風：",
        ["正式", "學術", "口語", "簡潔摘要", "可愛風"]
    )

if st.button("🚀 執行任務"):

    if selected_mode == "📌 問答模式":
        if not db:
            st.error("請先上傳文件！")
        else:
            docs = db.similarity_search(user_input, k=3)
            context = "\n".join([d.page_content for d in docs])
            prompt = f"根據以下內容回答問題：\n{context}\n\n問題：{user_input}\n\n回答："
            st.write(llm(prompt))

    elif selected_mode == "📝 摘要模式":
        prompt = f"請用繁體中文摘要以下內容：\n{text[:3000]}"
        st.write(llm(prompt))

    elif selected_mode == "✍️ 文風改寫模式":
        rewrite_prompt = f"請將以下內容以【{tone}】風格重寫，輸出繁體中文：\n{user_input}"
        st.write(llm(rewrite_prompt))