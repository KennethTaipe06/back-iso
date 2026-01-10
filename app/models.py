from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base  # Importamos Base desde database.py

class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String)
    descripcion = Column(Text)
    usuarios = relationship("Usuario", back_populates="rol")

    def __str__(self):
        return self.nombre_rol

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    estado = Column(String)
    
    rol = relationship("Rol", back_populates="usuarios")
    documentos_subidos = relationship("Documento", back_populates="usuario_subida")
    historial_modificaciones = relationship("HistorialVersiones", back_populates="usuario_modifico")

    def __str__(self):
        return self.nombre_completo

class ControlISO(Base):
    __tablename__ = "controles_iso"
    id_control = Column(Integer, primary_key=True, index=True)
    codigo_norma = Column(String)
    codigo_control = Column(String)
    descripcion = Column(Text)
    documento_relaciones = relationship("DocumentoControl", back_populates="control")

    def __str__(self):
        return f"{self.codigo_norma} - {self.codigo_control}"

class Documento(Base):
    __tablename__ = "documentos"
    id_documento = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    ruta_archivo = Column(String)
    tipo_documento = Column(String)
    proceso_asociado = Column(String)
    version_actual = Column(String)
    id_usuario_subida = Column(Integer, ForeignKey("usuarios.id_usuario"))
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    contenido_texto_ia = Column(Text)

    usuario_subida = relationship("Usuario", back_populates="documentos_subidos")
    controles_asociados = relationship("DocumentoControl", back_populates="documento")
    historial = relationship("HistorialVersiones", back_populates="documento")

    def __str__(self):
        return self.titulo

class DocumentoControl(Base):
    __tablename__ = "documento_controles"
    id_relacion = Column(Integer, primary_key=True, index=True)
    id_documento = Column(Integer, ForeignKey("documentos.id_documento"))
    id_control = Column(Integer, ForeignKey("controles_iso.id_control"))
    origen_asignacion = Column(String)
    confirmado = Column(Boolean, default=False)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)

    documento = relationship("Documento", back_populates="controles_asociados")
    control = relationship("ControlISO", back_populates="documento_relaciones")

class HistorialVersiones(Base):
    __tablename__ = "historial_versiones"
    id_historial = Column(Integer, primary_key=True, index=True)
    id_documento = Column(Integer, ForeignKey("documentos.id_documento"))
    version = Column(String)
    fecha_cambio = Column(DateTime, default=datetime.utcnow)
    id_usuario_modifico = Column(Integer, ForeignKey("usuarios.id_usuario"))
    ruta_archivo_version = Column(String)

    documento = relationship("Documento", back_populates="historial")
    usuario_modifico = relationship("Usuario", back_populates="historial_modificaciones")