import streamlit as st
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Models
llm = Ollama(model="qwen2.5:1.5b")
embed_model = OllamaEmbeddings(model="bge-m3")

st.title("📚 NLP AI Assistant — RAG + Summary + Rewrite")

uploaded_file = st.file_uploader("上傳 PDF/TXT 文件", type=["pdf", "txt"])

if uploaded_file:
    st.success("文件已上傳，正在處理...")

    text = ""

    if uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            text += page.extract_text()
    else:
        text = uploaded_file.read().decode("utf-8")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    db = Chroma.from_texts(chunks, embed_model)

    option = st.selectbox(
        "選擇模式",
        ["問答模式", "摘要模式", "文風改寫模式"]
    )

    user_input = st.text_input("輸入問題 / 句子：")

    if st.button("執行"):
        if option == "問答模式":
            docs = db.similarity_search(user_input, k=3)
            context = "\n".join([d.page_content for d in docs])
            prompt = f"根據以下內容回答：\n{context}\n\n問題：{user_input}\n回答："
            st.write(llm(prompt))

        elif option == "摘要模式":
            prompt = f"請用繁體中文摘要以下內容：\n{text[:2000]}..."
            st.write(llm(prompt))

        elif option == "文風改寫模式":
            prompt = f"請將以下文字改為更自然但正式的語氣：\n{user_input}"
            st.write(llm(prompt))