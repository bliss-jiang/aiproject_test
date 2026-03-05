import pickle
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.question_answering import load_qa_chain
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List, Tuple
from dotenv import load_dotenv
import os


load_dotenv()
EMBEDDING_DIM = 1024
COLLECTION_NAME = "full_demo"
ATTACHMENT_PATH = "./attachments"
QDRANT_PATH = "./qdrant_db"
FAISS_PATH = "./faiss_db"
LOCAL_API_KEY = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"
AUTH_HEADER = {"Authorization": f"Bearer {LOCAL_API_KEY}"}
BASE_URL="http://192.168.18.201:9453"
BASE_LLM_URL="http://192.168.18.201:9453/v1"
EMBED_MODEL="bge-m3:latest"
LLM_MODEL="gemma3:latest"


def load_base_knowledge(path:str,embeddings=None)->FAISS:
    if embeddings is None:
        embeddings = OllamaEmbeddings(
            base_url=BASE_URL,
            model=EMBED_MODEL
        )

    # 加载FAISS向量数据库，添加allow_dangerous_deserialization=True参数以允许反序列化
    base_knowledge = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    print(f"向量数据库已从 {path} 加载。")

    page_info_path = os.path.join(path, "page_info.pkl")
    if os.path.exists(page_info_path):
        with open(page_info_path, "rb") as f:
            page_info = pickle.load(f)
        base_knowledge.page_info = page_info
        print("页码信息已加载。")
    else:
        print("警告: 未找到页码信息文件。")
    return base_knowledge

def query_document_ai_langchain(query:str,embeddings=None)->str:
    query_knowledge = load_base_knowledge(FAISS_PATH)
    back_query = ""
    if query:
        query_docs = query_knowledge.similarity_search(query,k=5)
        print("similarity_search 搜索的结果是：")
        for query_doc in query_docs:
            print(query_doc.page_content[:500])
            print("-------------------------------------------------------")
        print("以上是搜索的结果")

        chatLLM = ChatOpenAI(
            api_key=LOCAL_API_KEY,
            base_url=BASE_LLM_URL,
            model=LLM_MODEL,
        )
        prompt = ChatPromptTemplate.from_template("""
        根据以下已知信息回答问题：
        {context}
        问题：{question}
        """)

        # 加载问答链
        # chain = load_qa_chain(chatLLM, chain_type="stuff")
        chain = create_stuff_documents_chain(chatLLM, prompt)

        # 使用问答链进行查询
        input_data = {"question": query, "context": query_docs}

        response = chain.invoke(input=input_data)
        back_query = response
        # back_query = response["output_text"]
        print(f"以下是答案===================================================================")
        print(response)
        print(f"以上是答案===================================================================")
        print("来源:")

        # 记录唯一的页码
        unique_pages = set()
        # 显示每个文档块的来源页码
        for doc in query_docs:
            text_content = getattr(doc, "page_content", "")
            source_page = query_knowledge.page_info.get(
                text_content.strip(), "未知"
            )

            if source_page not in unique_pages:
                unique_pages.add(source_page)
                print(f"文本块页码: {source_page}")

    return back_query

def save_text_with_splitter_to_faiss(text: str,text_page_numbers: List[int]) -> FAISS:
    save_path = FAISS_PATH
    # 将文本内容向量化后存储到向量数据库中
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=512,
        chunk_overlap=128,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    print(f"save_text_with_splitter函数 分割后的文本块数量: {len(chunks)} 个块。")

    embeddings = OllamaEmbeddings(
        base_url=BASE_URL,
        model=EMBED_MODEL
    )

    new_docs = []
    page_numbers = []
    for i,chunk in enumerate(chunks):
        new_doc = Document(page_content=chunk,page_number=i+1,metadata={"source": "new"})
        new_docs.append(new_doc)
        page_numbers.append(i)
    page_info = {chunk: page_numbers[i] for i, chunk in enumerate(chunks)}

    if save_path:
        os.makedirs(save_path, exist_ok=True)
        try:
            print("正在加载旧索引...")
            db = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"未找到旧索引或加载失败 ({e})，正在创建新索引...")
            db = FAISS.from_documents(new_docs, embeddings)
        print("正在添加新数据...")
        db.add_documents(new_docs)
        db.page_info = page_info
        db.save_local(save_path)
        print(f"向量数据库已保存到: {save_path}")

        with open(os.path.join(save_path, "page_info.pkl"), "wb") as f:
            pickle.dump(page_info, f)
        print(f"页码信息已保存到: {os.path.join(save_path, 'page_info.pkl')}")

    return db

if __name__ == '__main__':
    pass