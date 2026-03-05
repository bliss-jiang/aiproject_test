from langchain_openai import OpenAIEmbeddings
import httpx
from langchain_community.embeddings import OllamaEmbeddings

custom_client = httpx.Client(
    headers={"Authorization": "Bearer DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"},
    timeout=120.0
)

# embeddings = OpenAIEmbeddings(
#     base_url="http://192.168.18.201:9453/v1/",
#     api_key="DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1",
#     model="bge-m3:latest", #bge-m3:latest
#     # chunk_size=1,
#     # http_client=custom_client,
# )

embeddings = OllamaEmbeddings(
    model="bge-m3:latest",
    base_url="http://192.168.18.201:9453"
)

try:
    vector = embeddings.embed_query("向量化测试")
    print(f"成功获取向量，维度: {len(vector)}")
    print(vector[:50])
except Exception as e:
    print(f"错误: {e}")
