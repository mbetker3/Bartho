from fastapi import FastAPI , UploadFile , File, HTTPException
from pydantic import BaseModel
import shutil
import os
import uuid
from pathlib import Path
import fitz  # PyMuPDF

app = FastAPI()

UPLOAD = Path("uploads")
UPLOAD.mkdir(exist_ok=True)

@app.post("/api/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
     # Save the uploaded file
    id = str(uuid.uuid4())
    name = f"{id}.pdf"
    file_path = UPLOAD / name
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        bytes_written = file_path.stat().st_size
    return {"filename": name, "id": id, "size": bytes_written}

@app.post("/api/render/{id}")
async def render_file(id: str):
    file_path = UPLOAD/f"{id}.pdf"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    scale = 2  # Zoom factor
    
    doc = fitz.open(file_path)
    num_pages = len(doc)
    images = []

    for page_num in range(num_pages):
        page = doc.load_page(page_num)

        pix = page.get_pixmap(matrix = fitz.Matrix(scale, scale)) 
        image_path = UPLOAD / f"{id}.page.{page_num + 1}.png"
        pix.save(image_path)
        images.append(str(image_path))

    doc.close()

    return {"file_id": id, "num_pages": num_pages, "images": images}





