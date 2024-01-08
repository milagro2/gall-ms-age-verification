import os
from fastapi import FastAPI

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
    app.run(debug=True, port=os.getenv("PORT", default=8000))
