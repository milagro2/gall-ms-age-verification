from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

# Ensure the application listens on 0.0.0.0:$PORT
if __name__ == "__main__":
    import os
    import uvicorn

    host = "0.0.0.0"
    port = int(os.getenv("PORT", default=8000))

    uvicorn.run(app, host=host, port=port)
