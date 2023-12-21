import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

# This block will only run if the script is executed directly, not imported
if __name__ == "__main__":
    import uvicorn

    # Get the port from the environment variable provided by Railway
    port = int(os.getenv("PORT", default=8000))

    # Run the Uvicorn server with the specified host and port
    uvicorn.run(app, host="0.0.0.0", port=port)
