import os
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, get_response_synthesizer
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core.postprocessor import LLMRerank, SimilarityPostprocessor
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama
import logging
import sys
from llama_index.core.callbacks import LlamaDebugHandler




def process_text_to_faiss_with_proxy(
        text: str,
        proxy_url: str = "http://192.168.18.201:9453",
        proxy_api_key: str = "DW5NEX6-HNHMY0D-MWXVGNK-9XY6KC1",
        save_path: str = "./faiss_index",
        model_name: str = "bge-m3:latest",
        chunk_size: int = 500,
        chunk_overlap: int = 50
) -> FAISS:

    embeddings = OllamaEmbeddings(
        model=model_name,
        base_url=proxy_url
    )
    print(f"正在分块 (Chunk Size: {chunk_size})...")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    texts = text_splitter.split_text(text)
    print(f"分块完成，共 {len(texts)} 块。")


    print("正在通过代理请求向量化并构建 FAISS 索引...")
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings)

    print(f"保存索引至: {save_path}")
    vector_store.save_local(save_path)

    return vector_store



if __name__ == "__main__":
    pass
    # sample_text = "这是一段测试文本。" * 100
    # db = process_text_to_faiss_with_proxy(
    #     text=sample_text
    # )
    # res = query_document_ai_llamaindex('LlamaIndex是什么？')