from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
import os

# Cria uma instância do FastAPI
app = FastAPI()

# Cria a pasta "uploads" se ela não existir
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Rota para servir o arquivo index.html com a lista de arquivos
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Lê o conteúdo do arquivo index.html
    with open("index.html", "r") as f:
        html_content = f.read()
    
    # Obtém a lista de arquivos na pasta "uploads"
    files = os.listdir(UPLOAD_DIR)
    file_links = ""
    for file in files:
        file_links += f'<li><a href="/download?filename={file}">{file}</a></li>'
    
    # Substitui o marcador {{file_list}} no HTML pelo conteúdo gerado
    html_content = html_content.replace("{{file_list}}", file_links)
    return HTMLResponse(content=html_content)

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
