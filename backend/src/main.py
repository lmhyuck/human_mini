import sys, uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", port=5000, reload=True)
    except Exception as e:
        sys.exit(1)