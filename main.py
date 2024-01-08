import os
from fastapi import FastAPI, File, UploadFile

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

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))
