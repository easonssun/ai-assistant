import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus

# --- 配置 ---
FILE_PATH = "../files/test.md" # 可以替换为你的PDF文件路径，如 "./my_document.pdf"
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "LangChainDemo")

# --- 初始化嵌入模型 ---
def initEmbeddings():
    print("正在加载嵌入模型...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("嵌入模型加载完成")
    return embeddings

Embeddings = initEmbeddings()

# --- 连接 Milvus ---
VectorStore = Milvus(
    embedding_function=Embeddings,
    collection_name=COLLECTION_NAME,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
)

def getLoader(file_path: str):
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path)
    else:
        return TextLoader(file_path, encoding="utf-8")

def loadDocuments(file_path: str):
    loader = getLoader(file_path)
    documents = loader.load()
    print(f"成功加载文件: {file_path}")
    return documents

documents = loadDocuments(loader, FILE_PATH)

# --- 2. 文本切分 ---
def splitDocuments(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    print(f"文档被切分为 {len(docs)} 个块")
    return docs

docs = splitDocuments(documents)


def initVectors(docs: list[Document]):
    print(f"正在将数据存入 Milvus 集合 '{COLLECTION_NAME}'...")
    # VectorStore.add_documents(docs)
    VectorStore.from_documents(docs)
    print("数据成功存入 Milvus")