import uvicorn
from fastapi import (
    status,
    FastAPI,
    Response
)
from extractor import extract as textract

app = FastAPI()


@app.get("/")
async def home():
    return {'message': '✅ ChatParser is running!'}


@app.get("/api/v1/extract")
async def extract(response:Response, url: str, list: bool = False):
    try:
        return textract(url, list)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': str(e)}

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="localhost",
        port=8000,
        reload=True
    )
