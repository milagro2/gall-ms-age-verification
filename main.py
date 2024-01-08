import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
    
@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

@app.post("/get_dimensions")
async def get_dimensions(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        width, height = image.size
        return JSONResponse(content={"width": width, "height": height}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))
