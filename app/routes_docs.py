from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session, joinedload
from .database import get_db
from .models import Documento, DocumentoControl, ControlISO, Usuario
from pydantic import BaseModel
from datetime import datetime
import shutil
import os

router = APIRouter(prefix="/api/documentos", tags=["Documentos"])

# --- Schema de Salida ---
class DocumentoOut(BaseModel):
    id_documento: int
    titulo: str
    tipo: str
    version: str
    fecha: datetime
    controles: List[str]
    url: Optional[str] = None # Permitimos que sea null

    class Config:
        from_attributes = True

# --- Endpoint GET (Listado) ---
@router.get("/", response_model=List[DocumentoOut])
def obtener_documentos(db: Session = Depends(get_db)):
    docs_db = db.query(Documento).options(
        joinedload(Documento.controles_asociados).joinedload(DocumentoControl.control)
    ).order_by(Documento.fecha_subida.desc()).all()
    
    resultado = []
    for doc in docs_db:
        codigos = [r.control.codigo_control for r in doc.controles_asociados if r.control]
        
        # --- CORRECCIÓN AQUÍ ---
        if doc.ruta_archivo:
            ruta_web = doc.ruta_archivo.replace("\\", "/")
            url_final = f"/{ruta_web}"
        else:
            url_final = None
        # -----------------------

        resultado.append({
            "id_documento": doc.id_documento,
            "titulo": doc.titulo,
            "tipo": doc.tipo_documento,
            "version": doc.version_actual,
            "fecha": doc.fecha_subida,
            "controles": list(set(codigos)), # Eliminamos duplicados
            "url": url_final
        })
    return resultado

# --- Endpoint GET (Detalle) ---
@router.get("/{id_doc}", response_model=DocumentoOut)
def obtener_documento_detalle(id_doc: int, db: Session = Depends(get_db)):
    doc = db.query(Documento).options(
        joinedload(Documento.controles_asociados).joinedload(DocumentoControl.control)
    ).filter(Documento.id_documento == id_doc).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
        
    codigos = [r.control.codigo_control for r in doc.controles_asociados if r.control]
    
    # --- CORRECCIÓN AQUÍ TAMBIÉN ---
    if doc.ruta_archivo:
        ruta_web = doc.ruta_archivo.replace("\\", "/")
        url_final = f"/{ruta_web}"
    else:
        url_final = None
    # -------------------------------
    
    return {
        "id_documento": doc.id_documento,
        "titulo": doc.titulo,
        "tipo": doc.tipo_documento,
        "version": doc.version_actual,
        "fecha": doc.fecha_subida,
        "controles": list(set(codigos)),
        "url": url_final
    }

# --- Endpoint POST (Guardar) ---
@router.post("/")
async def subir_documento(
    titulo: str = Form(...),
    tipo: str = Form(...),
    proceso: str = Form(...),
    version: str = Form(...),
    control_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    usuario = db.query(Usuario).first()
    id_usuario = usuario.id_usuario if usuario else 1

    nuevo_doc = Documento(
        titulo=titulo,
        tipo_documento=tipo,
        proceso_asociado=proceso,
        version_actual=version,
        ruta_archivo=file_location,
        id_usuario_subida=id_usuario,
        fecha_subida=datetime.utcnow()
    )
    db.add(nuevo_doc)
    db.commit()
    db.refresh(nuevo_doc)

    control_obj = db.query(ControlISO).filter(ControlISO.codigo_control == control_id).first()
    if control_obj:
        relacion = DocumentoControl(
            id_documento=nuevo_doc.id_documento,
            id_control=control_obj.id_control,
            confirmado=True
        )
        db.add(relacion)
        db.commit()

    return {"mensaje": "Guardado", "id": nuevo_doc.id_documento}