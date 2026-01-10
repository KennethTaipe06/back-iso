from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # <--- 1. IMPORTAR ESTO
import os

from .database import engine, Base
from .admin import setup_admin
from .routes_auth import router as auth_router
from .routes_docs import router as docs_router

# Crear carpeta uploads si no existe
os.makedirs("uploads", exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestor Documental ISO")

# Configuración CORS (Igual que antes)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. AGREGAR ESTA LÍNEA PARA SERVIR LOS PDF ---
# Esto hace que http://localhost:8000/uploads/archivo.pdf sea accesible
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# ------------------------------------------------

setup_admin(app, engine)
app.include_router(auth_router)
app.include_router(docs_router)

@app.get("/")
def read_root():
    return {"mensaje": "API ISOOne corriendo"}