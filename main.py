from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os

# Cria uma instância do FastAPI
app = FastAPI()

# Cria a pasta "uploads" se ela não existir
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Rota para servir o arquivo index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Rota para upload de arquivos
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Salva o arquivo na pasta "uploads"
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"File '{file.filename}' uploaded successfully."}

# Rota para download de arquivos
@app.get("/download")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path, filename=filename)
