from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# --- CONFIGURACIÓN DE BASE DE DATOS ---
# Usar Connection Pooler de Supabase (puerto 6543) con modo session
# Contraseña URL-encoded: R.vg#htM*V6C@x! → R.vg%23htM%2AV6C%40x%21
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:R.vg%23htM%2AV6C%40x%21@db.pqlvvbggwennzfcqxvdo.supabase.co:6543/postgres"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c timezone=utc"
    },
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de DB (se usará en los endpoints después)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()