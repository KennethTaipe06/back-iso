from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost/mi_base_de_datos"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de DB (se usará en los endpoints después)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()