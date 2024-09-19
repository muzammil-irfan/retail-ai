from fastapi import FastAPI, HTTPException
from typing import Optional, AsyncIterator
from .database import create_db_and_tables, engine
from sqlmodel import Session, select
from .models import StoreSales
# lifespan function
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        create_db_and_tables()
        yield
    except Exception as e:
        print(f"Error during startup: {e}")

# Initialize the FastAPI app
app = FastAPI(title="Panaversity User Management and Authentication", 
    version="0.0.1",
    servers=[
            {
                "url": "http://localhost:8005", # ADD NGROK URL Here Before Creating GPT Action
                "description": "Development Server"
            },
            {
                "url": "http://localhost:8000",
                "description": "Production Server"
            }
        ]
    ) 


@app.get("/")
def hello_world():
    return {"Hello":"World"}

@app.get("/sales")
def read_sales(store_id: int = None, dept_id: int = None):
    with Session(engine) as session:
        query = select(StoreSales)
        if store_id:
            query = query.where(StoreSales.store_id == store_id)
        if dept_id:
            query = query.where(StoreSales.dept_id == dept_id)
        results = session.exec(query).all()
        return results
    
# # Initialize Google Cloud Language client
# client = language.LanguageServiceClient()

# # Define Pydantic model for text analysis request
# class TextAnalysisRequest(BaseModel):
#     text: str

# # Define Pydantic model for text analysis response
# class TextAnalysisResponse(BaseModel):
#     sentiment: dict
#     entities: list
#     language: str

# # Route for text analysis
# @app.post("/analyze", response_model=TextAnalysisResponse)
# async def analyze_text(request: TextAnalysisRequest):
#     try:
#         # Create a Language API document
#         document = language.Document(content=request.text, type_=language.Document.Type.PLAIN_TEXT)

#         # Analyze the text using the Language API
#         response = client.analyze_text(document=document, encoding_type='UTF8')

#         # Extract sentiment, entities, and language from the response
#         sentiment = response.sentiment
#         entities = response.entities
#         language = response.language

#         # Return the text analysis response
#         return JSONResponse(content={"sentiment": sentiment, "entities": entities, "language": language}, media_type="application/json")

#     except Exception as e:
#         # Raise an HTTP exception if an error occurs
#         raise HTTPException(status_code=500, detail=str(e))