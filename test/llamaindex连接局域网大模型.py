from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama

# 1. 配置 LLM (大语言模型)
# 将 base_url 替换为你局域网中 Ollama 服务的实际 IP 和端口
API_KEY = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1"
# 常见的格式是 Bearer Token，如果是自定义 Key，直接填值即可
AUTH_HEADER = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL="http://192.168.18.201:9453"
ollama_client = ollama.Client(
    host=BASE_URL,
    headers={'Authorization': f'Bearer {API_KEY}'} # 注意：这里必须是字典格式
)

Settings.llm = Ollama(
    model="gemma3:latest",  # 确保你在 ollama 中 pull 了这个模型
    client=ollama_client, # <--- 关键：直接传入配置好的 client
    base_url="http://192.168.18.201:9453/v1",  # 局域网地址
    request_timeout=120.0  # 如果模型很大，生成可能较慢，适当增加超时时间
)

# 2. 配置 Embed Model (嵌入模型)
Settings.embed_model = OllamaEmbedding(
    model_name="bge-m3:latest",
    client=ollama_client,
    base_url="http://192.168.18.201:9453",  # 局域网地址
)

# 3. 测试配置是否生效
# 现在你可以直接创建 Index，而不需要每次都传入 llm 和 embed_model 参数
from llama_index.core import VectorStoreIndex, Document

# 创建一个简单的文档进行测试
documents = [Document(text="LlamaIndex 是一个连接大语言模型和私有数据的框架。")]

# 创建索引 (会自动使用上面设置的 Settings)
index = VectorStoreIndex.from_documents(documents)

# 创建查询引擎
query_engine = index.as_query_engine()

# 执行查询
response = query_engine.query("LlamaIndex 是做什么的？")
print(response)
