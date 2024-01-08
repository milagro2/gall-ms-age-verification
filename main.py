import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}


@app.get("/get_dimensions")
def read_hello():
    return {"message": "Bye Bye!"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
