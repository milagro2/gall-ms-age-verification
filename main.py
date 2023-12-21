import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", default=5000))

    uvicorn.run(app, host="0.0.0.0", port=port)
