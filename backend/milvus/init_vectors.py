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

# --- 1. 加载文件 ---
# 根据文件扩展名选择不同的加载器
if FILE_PATH.endswith(".pdf"):
    loader = PyPDFLoader(FILE_PATH)
else:
    loader = TextLoader(FILE_PATH, encoding="utf-8")

documents = loader.load()
print(f"成功加载文件: {FILE_PATH}")

# --- 2. 文本切分 ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
print(f"文档被切分为 {len(docs)} 个块")

# --- 3. 初始化嵌入模型 ---
print("正在加载嵌入模型...")
embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
print("嵌入模型加载完成")

# --- 4. 存入 Milvus ---
print(f"正在将数据存入 Milvus 集合 '{COLLECTION_NAME}'...")
vector_store = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
    drop_old=True
)
print("数据成功存入 Milvus")

# --- 5. 验证与查询 ---
db = Milvus(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
)

query = "机器学习的核心是什么？"
print(f"\n执行查询: '{query}'")

results = db.similarity_search(query, k=2)

print("搜索结果:")
for i, doc in enumerate(results):
    print(f"\n--- 结果 {i+1} ---")
    print(f"内容: {doc.page_content}")
