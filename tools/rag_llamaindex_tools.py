from dotenv import load_dotenv
from llama_index.core.callbacks import LlamaDebugHandler
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, get_response_synthesizer
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core.postprocessor import LLMRerank, SimilarityPostprocessor
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama

load_dotenv()

EMBEDDING_DIM = 1024
COLLECTION_NAME = "full_demo"
ATTACHMENT_PATH = "./attachments"
QDRANT_PATH = "./qdrant_db"
FAISS_PATH = "./faiss_db"
client = QdrantClient(path=QDRANT_PATH)
LOCAL_API_KEY = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"
AUTH_HEADER = {"Authorization": f"Bearer {LOCAL_API_KEY}"}
BASE_URL="http://192.168.18.201:9453"
BASE_LLM_URL="http://192.168.18.201:9453/v1"
EMBED_MODEL="bge-m3:latest"
LLM_MODEL="gemma3:latest" #llama3.2:latest/gemma3:latest

def query_document_ai_llamaindex(question:str)->str:
    print("llamaindex 开始")
    ollama_client = ollama.Client(
        host=BASE_URL,
        headers=AUTH_HEADER  # 注意：这里必须是字典格式
    )
    # 1. 指定全局llm与embedding模型
    Settings.llm = Ollama(
        model=LLM_MODEL,
        client=ollama_client,  #直接传入配置好的 client
        base_url=BASE_LLM_URL,
        request_timeout=300.0
    )

    Settings.embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        client=ollama_client,
        base_url=BASE_URL,
    )
    # 2. 指定全局文档处理的 Ingestion Pipeline
    Settings.transformations = [SentenceSplitter(chunk_size=512, chunk_overlap=200)]

    # 3. 加载本地文档
    documents = SimpleDirectoryReader("./attachments").load_data()

    if not client.collection_exists(collection_name=COLLECTION_NAME):
        print("创建集合")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
        )

        # 5. 创建 Vector Store
        vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)

        # 6. 指定 Vector Store 的 Storage 用于 index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
    else:
        vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents([], storage_context=storage_context)

        # 7. 定义检索后排序模型
    reranker = LLMRerank(top_n=2)
    # 最终打分低于0.6的文档被过滤掉
    sp = SimilarityPostprocessor(similarity_cutoff=0.6)

    # 8. 定义 RAG Fusion 检索器
    fusion_retriever = QueryFusionRetriever(
        [index.as_retriever()],
        similarity_top_k=3,  # 检索召回 top k 结果
        num_queries=3,  # 生成 query 数
        use_async=False,
        # query_gen_prompt="",  # 可以自定义 query 生成的 prompt 模板
    )

    # 9. 构建单轮 query engine
    query_engine = RetrieverQueryEngine.from_args(
        fusion_retriever,
        node_postprocessors=[sp],
        response_synthesizer=get_response_synthesizer(
            response_mode=ResponseMode.COMPACT #ResponseMode.COMPACT 紧凑模式COMPACT/精炼模式REFINE
        )
    )

    # 10. 对话引擎
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        # condense_question_prompt="" # 可以自定义 chat message prompt 模板
    )

    response = chat_engine.chat(question)
    print(f"AI: {response}")
    # client.close()
    return response.response


def query_document_ai_llamaindex_embed(question:str)->str:
    import ollama

    # 保存原始 chat 方法
    original_chat = ollama.Client.chat
    # 定义补丁
    def patched_chat(self, model, messages, **kwargs):
        print(f"\n>>> [Ollama拦截] 模型: {model}")
        print(f">>> [Ollama拦截] 输入消息: {messages}\n")
        # 调用原始方法
        result = original_chat(self, model, messages, **kwargs)
        print(f">>> [Ollama拦截] 输出结果: {result}\n")
        return result
    ollama.Client.chat = patched_chat

    print("llamaindex 开始")
    ollama_client = ollama.Client(
        host=BASE_URL,
        headers=AUTH_HEADER  # 注意：这里必须是字典格式
    )
    # 1. 指定全局llm与embedding模型
    Settings.llm = Ollama(
        model=LLM_MODEL,
        client=ollama_client,  # 直接传入配置好的 client
        base_url=BASE_LLM_URL,
        request_timeout=120.0
    )

    Settings.embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        client=ollama_client,
        base_url=BASE_URL,  # 局域网地址
    )
    # 2. 指定全局文档处理的 Ingestion Pipeline
    Settings.transformations = [SentenceSplitter(chunk_size=512, chunk_overlap=200)]

    # 3. 加载本地文档
    documents = SimpleDirectoryReader("./attachments").load_data()
    # print(documents)
    if client.collection_exists(collection_name=COLLECTION_NAME):
        client.delete_collection(collection_name=COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
    )

    # 5. 创建 Vector Store
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)

    # 6. 指定 Vector Store 的 Storage 用于 index
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    # 7. 定义检索后排序模型
    reranker = LLMRerank(top_n=2)
    sp = SimilarityPostprocessor(similarity_cutoff=0.4)

    query_gen_prompt_str = (
        "You are a helpful assistant designed to generate multiple search queries based on a single input query.\n"
        "Your task is to generate {num_queries} search queries related to the following input query.\n"
        "CRITICAL RULE: The output MUST be a valid JSON list of strings.\n"
        "Do NOT include any other text, explanations, or markdown formatting (like ```json).\n"
        "Example Output: [\"search query 1\", \"search query 2\"]\n\n"
        "Input Query: {query}\n"  
        "Queries:\n"
    )
    # 8. 定义 RAG Fusion 检索器
    fusion_retriever = QueryFusionRetriever(
        [index.as_retriever()],
        similarity_top_k=3,  # 检索召回 top k 结果
        num_queries=4,  # 生成 query 数
        use_async=False,
        verbose=True #开启日志
        # query_gen_prompt=query_gen_prompt_str,  # 可以自定义 query 生成的 prompt 模板
    )

    # 9. 构建单轮 query engine
    query_engine = RetrieverQueryEngine.from_args(
        fusion_retriever,
        node_postprocessors=[sp],
        response_synthesizer=get_response_synthesizer(
            response_mode=ResponseMode.COMPACT #ResponseMode.COMPACT 紧凑模式COMPACT/精炼模式REFINE
        )
    )

    # 10. 对话引擎
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        # condense_question_prompt="" # 可以自定义 chat message prompt 模板
    )

    response = chat_engine.chat(question)
    print(f"AI: {response}")

    return response.response


if __name__ == '__main__':
    res = query_document_ai_llamaindex("星期二下午上什么课？")
    print(res)