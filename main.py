from fastapi import FastAPI
from fastapi import UploadFile,File
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import HTMLResponse
from tools.file_tools import (
    get_file_txt_content,
    get_file_docx_content,
    save_upload_file,
    extract_pdf_text_with_page_numbers
)
from tools.rag_langchain_tools import (
    save_text_with_splitter_to_faiss,
    query_document_ai_langchain,
)
from tools.rag_llamaindex_tools import (
    query_document_ai_llamaindex,
    query_document_ai_llamaindex_embed
)
app = FastAPI()
app.mount("/html", StaticFiles(directory="html"), name="html")


@app.post("/upload_file/")
async def upload_file(fileInput: UploadFile = File(...)):
    file_extension = Path(fileInput.filename).suffix.lower()
    file_status = save_upload_file(fileInput)
    file_name = file_status["file_name"]
    if file_status["status"] == "successfully":
        if file_extension in [".pdf"]:
            pdf_text, page_numbers = extract_pdf_text_with_page_numbers(file_name)
            save_text_with_splitter_to_faiss(pdf_text, page_numbers)
            return file_status["status"]
        elif file_extension in [".txt"]:
            txt_text = get_file_txt_content(file_name)
            if txt_text is not None:
                save_text_with_splitter_to_faiss(txt_text, [])
            return file_status["status"]
        elif file_extension in [".docx"]:
            docx_text = get_file_docx_content(file_name)
            print(docx_text)
            if docx_text is not None:
                save_text_with_splitter_to_faiss(docx_text, [])
            return file_status["status"]
        return "successfully"
    else:
        return file_status["status"]

@app.get("/chatquery")
async def chat_query(query_text:str,scheme:str):
    if scheme == "LlamaIndex":
        query_result = query_document_ai_llamaindex_embed(query_text)
        return {"query_result" : query_result}
    elif scheme == "langchain":
        query_result = query_document_ai_langchain(query_text)
        return {"query_result": query_result}
    return {"query_result": "未选择搜寻方案..."}

@app.get("/aichats/")
async def new_chat():
    return HTMLResponse(content=open("html/MultiAI_Chat.html", "r",encoding="utf-8").read(), status_code=200)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8888)