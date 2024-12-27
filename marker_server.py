# /app/marker_server.py

from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
import os

# Marker imports
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

app = FastAPI()

# Initialize marker artifacts once (to avoid reloading in each request)
converter = PdfConverter(artifact_dict=create_model_dict())

@app.get("/")
def root():
    return {"message": "Marker server is running!"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    print("start_convert")
    temp_filepath = f"/tmp/{file.filename}"
    with open(temp_filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    rendered = converter(temp_filepath)

    text, m, images = text_from_rendered(rendered)
    print(text)
    print(m)
    print(images)
    os.remove(temp_filepath)
    return {"markdown": text, "images": images}

if __name__ == "__main__":
    uvicorn.run("marker_server:app", host="0.0.0.0", port=8000)
