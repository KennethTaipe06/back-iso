from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Esquemas para Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Esquemas para Usuario ---
class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    nombre_completo: str
    password: str
    id_rol: int = 2  # Por defecto: Usuario (1=Administrador, 2=Usuario, 3=Auditor)

class UsuarioOut(UsuarioBase):
    id_usuario: int
    nombre_completo: str
    estado: Optional[str] = None
    
    class Config:
        from_attributes = True # Esto permite leer directo del modelo SQLAlchemy