from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(
    title="vector-search-backend"
    description=""
    version=""
)

@app.post("/search", description="Search the vector store through this endpoint.")
def search(query: str):
    return JSONResponse(content={"Your query": query}, status_code=200)

# --- 
# TODO: HEMMINGWAY 
# - create a few production ready routes for
#   - asking a question
#   - getting a regurgitation of the question asked
#   - getting a list of resutls (chunks) with metadata 
# - work on it until it seems to produce really good results
# 
# Other than ensure compatible JSON format responses, 
# wait until this is done to go back to the front end. 
# --- 