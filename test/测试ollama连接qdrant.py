import ollama
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

# 配置部分
OLLAMA_HOST = "http://192.168.18.201:9453"
API_KEY = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"
EMBED_MODEL = "bge-m3:latest"
CHAT_MODEL = "gemma3:latest"
COLLECTION_NAME = "my_documents"


def process_text_to_qdrant_with_llamaindex(query_text):
    import ollama
    import httpx
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    import uuid

    # 配置
    OLLAMA_HOST = "http://192.168.18.201:9453"
    API_KEY = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"
    EMBED_MODEL = "bge-m3:latest"
    CHAT_MODEL = "gemma3:latest"
    COLLECTION_NAME = "my_documents"

    # 1. 初始化 Ollama
    client = ollama.Client(
        host=OLLAMA_HOST,
        headers={'Authorization': f'Bearer {API_KEY}'},
        timeout=120.0
    )

    # 2. 初始化 Qdrant
    qdrant = QdrantClient(":memory:")

    # 3. 确保 Collection 存在
    try:
        test_embed = client.embed(model=EMBED_MODEL, input="test")
        vector_dim = len(test_embed["embeddings"][0])
    except Exception as e:
        print(f"获取 Embedding 维度失败: {e}")
        return

    collections = qdrant.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE)
        )
        print(f"创建集合: {COLLECTION_NAME}")

    # 4. 插入数据
    docs = [
        {"id": str(uuid.uuid4()), "text": "LlamaIndex 是一个数据框架，用于连接大语言模型。",
         "metadata": {"source": "intro"}},
        {"id": str(uuid.uuid4()), "text": "Ollama 允许你在本地运行大模型，如 Llama3 和 Gemma。",
         "metadata": {"source": "tools"}},
    ]

    points = []
    for doc in docs:
        response = client.embed(model=EMBED_MODEL, input=doc["text"])
        embedding = response["embeddings"][0]
        points.append(PointStruct(
            id=doc["id"],
            vector=embedding,
            payload={"text": doc["text"], "metadata": doc["metadata"]}
        ))

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print("数据已插入 Qdrant")

    # 5. 检索 (修改部分)
    query_embedding_response = client.embed(model=EMBED_MODEL, input=query_text)
    query_vector = query_embedding_response["embeddings"][0]

    # 使用 query_points 以兼容更多版本
    try:
        search_result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=2
        )
        # 兼容性提取结果
        points = search_result.points if hasattr(search_result, 'points') else []
    except AttributeError:
        # 如果 query_points 也不存在，尝试使用旧的 search (虽然报错说没有，但以防万一)
        # 或者直接报错
        print("当前 Qdrant 客户端版本不支持 query_points，请升级 qdrant-client")
        return "客户端版本过低"

    if not points:
        return "未找到相关信息。"

    context_text = "\n\n".join([hit.payload["text"] for hit in points])

    # 6. 生成回答
    prompt = f"""
    基于以下上下文信息回答问题。如果上下文中没有答案，请说不知道。

    上下文:
    {context_text}

    问题: {query_text}
    """

    response = client.chat(
        model=CHAT_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=False
    )

    return response['message']['content']


# 测试调用
if __name__ == '__main__':
    res = process_text_to_qdrant_with_llamaindex('LlamaIndex 是做什么的？')
    print("-" * 20)
    print("最终回答:")
    print(res)
