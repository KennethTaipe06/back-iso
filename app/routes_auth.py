from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from .models import Usuario
from .schemas import UsuarioCreate, Token, UsuarioOut
from .security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=Token)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar si existe
    user_exist = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # 2. Crear usuario
    hashed_pw = get_password_hash(usuario.password)
    nuevo_usuario = Usuario(
        email=usuario.email,
        nombre_completo=usuario.nombre_completo,
        password_hash=hashed_pw,
        id_rol=usuario.id_rol,
        estado="ACTIVO"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # 3. Retornar Token directo
    access_token = create_access_token(data={"sub": nuevo_usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscamos por email (form_data.username contendrá el email)
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email, "id": user.id_usuario})
    return {"access_token": access_token, "token_type": "bearer"}