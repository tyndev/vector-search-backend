from langchain_qdrant import Qdrant
from langchain_openai  import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader

from qdrant_client import QdrantClient, models

from dotenv import load_dotenv
import os

load_dotenv()


qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv('QDRANT_URL')
collection_name = "Standards"

openai_api_key = os.getenv('OPENAI_API_KEY')

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=OpenAIEmbeddings(
        api_key=openai_api_key
    )
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=20, 
    length_function=len
)

def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
    )
    print(f"{collection_name} Collection created successfully")
    
def upload_standard_to_collection(url:str):
    # TODO: add prevent duplicate standards function (likely a separate db)
    # that checks if a document (with its version) has already been uploaded.
    loader = PDFPlumberLoader(url) # Online link to standard PDF
    chunks = loader.load_and_split(text_splitter)
    for chunk in chunks:
        chunk.metadata = {"source": url}
    vector_store.add_documents(chunks)
    print(f"Successfully uploaded {len(chunks)} chunks to {collection_name} Collection")

# These must be off before using the search/chat feature in rag.py
# create_collection(collection_name) # only needed to create a new collection of vectors
# upload_standard_to_collection("https://www.nerc.com/pa/Stand/Reliability%20Standards/PRC-025-2.pdf") # only do this once per documents