from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from dotenv import load_dotenv
from mock_data import get_mock_data_response
from models import ResponseBody

load_dotenv()

app = FastAPI()


origins = json.loads(os.getenv("ALLOWED_ORIGINS", '[]'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchResult(BaseModel):
    id:str
    title: str
    summary: str
    url: str

class SearchTip(BaseModel):
    id:str
    tip: str
    
mock_documents = [
    SearchResult(
        id="std101",
        title="IEEE 1547-2018 Standard for Interconnection and Interoperability of Distributed Energy Resources",
        summary="This standard provides technical specifications for the interconnection and interoperability of distributed resources with electric power systems. It covers voltage regulation, response to system disturbances, and communication protocols for enhanced integration.",
        url="https://example.com/IEEE1547-2018"
    ),
    SearchResult(
        id="std102",
        title="ANSI C84.1 Electric Power Systems and Equipment - Voltage Ranges",
        summary="ANSI C84.1 specifies the voltage ratings for electric power systems and equipment in North America. It defines nominal voltage ranges and tolerances for both the transmission and the distribution of alternating current.",
        url="https://example.com/ANSIC84.1"
    ),
    SearchResult(
        id="std103",
        title="IEC 61850 Communication Networks and Systems for Power Utility Automation",
        summary="IEC 61850 is an international standard detailing the communication networks and systems for substations automation. It includes protocols for real-time communication between field devices and control systems, enhancing reliability and performance.",
        url="https://example.com/IEC61850"
    ),
    SearchResult(
        id="std104",
        title="IEEE 1676-2010 - IEEE Guide for Control Architecture for High Power Electronics",
        summary="IEEE 1676-2010 provides guidelines for the control architecture of high-power electronics (1 MW and greater) used in electric power systems, including design considerations and performance metrics.",
        url="https://example.com/IEEE1676-2010"
    ),
    SearchResult(
        id="std105",
        title="NFPA 70: National Electrical Code (NEC) 2020",
        summary="The NEC 2020 is essential for safe electrical design, installation, and inspection to protect people and property from electrical hazards. This code covers the latest comprehensive regulations for electrical wiring, overcurrent protection, grounding, and installation of equipment.",
        url="https://example.com/NFPA70-2020"
    )
]

@app.get("/", response_model=ResponseBody)
def get_mock_data(query: Optional[str] = Query(None, min_length=1)) -> ResponseBody:
    return get_mock_data_response(query)

@app.get("/test")
async def read_root():
    environment = os.getenv("ENVIRONMENT", "production")  # Default to production if not set
    message = "Hello from local backend." if environment == "development" else "Hello from production backend."
    print(message)
    return {"message": message}

# @app.get("/search", response_model=List[SearchResult])
@app.get("/search-old")
async def search_old(query: Optional[str] = Query(None, min_length=3, max_length=50)):
    #TODO: Replaced simulated search response with rag query
    print(query)
    results = mock_documents
    return results


@app.get("/search-tips", response_model=List[SearchTip])
async def tips(query: Optional[str] = Query(None, max_length=50)):
    print(f"Search Tips requested for... {query}")
    search_tips = []
    if len(query or "") < 10:
        search_tips = [
            SearchTip(id="0", tip="Which document talks about top-rated utilities?"),
        ]
    elif len(query or "") >= 10:
        search_tips = [
            SearchTip(id="0", tip="Which document talks about top-rated utilities?"),
            SearchTip(id="1", tip="How does electricity work?")
        ]        
    return search_tips


