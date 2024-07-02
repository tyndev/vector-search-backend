from pydantic import BaseModel

class Metadata(BaseModel):
    source_url: str
    id: str
    collection_name: str

class Document(BaseModel):
    page_content: list[str]
    metadata: Metadata
    type: str

class ResponseBody(BaseModel):
    question: str
    results_summary: str
    documents: list[Document]
