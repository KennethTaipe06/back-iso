from app.database import SessionLocal, engine, Base
from app.models import ControlISO, Documento, DocumentoControl, Usuario, Rol
from app.security import get_password_hash
from datetime import datetime

# 1. Reiniciar Base de Datos (Borra todo y crea de nuevo)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("🌱 Iniciando carga MASIVA de ISO 27001...")

# --- 2. Crear Roles y Usuarios ---
rol_admin = Rol(nombre_rol="Admin", descripcion="Administrador del SGSI")
rol_user = Rol(nombre_rol="Colaborador", descripcion="Usuario de consulta")
db.add(rol_admin)
db.add(rol_user)
db.commit()

# Crear Usuario Admin por defecto
admin_user = Usuario(
    nombre_completo="Admin ISOOne",
    email="admin@isoone.com",
    password_hash=get_password_hash("admin123"), # Contraseña: admin123
    id_rol=rol_admin.id_rol,
    estado="ACTIVO"
)
db.add(admin_user)
db.commit()

# --- 3. CARGA DE CONTROLES ISO 27001 (ANEXO A) ---
# Lista oficial de dominios y controles clave
controles_iso = [
    # A.5 Políticas
    ("A.5", "5.1.1", "Políticas para la seguridad de la información"),
    ("A.5", "5.1.2", "Revisión de las políticas"),
    
    # A.6 Organización
    ("A.6", "6.1.1", "Roles y responsabilidades"),
    ("A.6", "6.1.2", "Segregación de funciones"),
    ("A.6", "6.2.1", "Dispositivos móviles y teletrabajo"),

    # A.7 Recursos Humanos
    ("A.7", "7.1.1", "Investigación de antecedentes"),
    ("A.7", "7.2.2", "Concienciación y formación"),
    ("A.7", "7.3.1", "Cese o cambio de empleo"),

    # A.8 Activos
    ("A.8", "8.1.1", "Inventario de activos"),
    ("A.8", "8.1.3", "Uso aceptable de los activos"),
    ("A.8", "8.2.1", "Clasificación de la información"),

    # A.9 Control de Acceso
    ("A.9", "9.1.1", "Política de control de acceso"),
    ("A.9", "9.2.1", "Alta y baja de usuarios"),
    ("A.9", "9.2.3", "Gestión de derechos de acceso privilegiado"),
    ("A.9", "9.4.1", "Restricción de acceso a la información"),

    # A.10 Criptografía
    ("A.10", "10.1.1", "Política de controles criptográficos"),

    # A.11 Seguridad Física
    ("A.11", "11.1.1", "Perímetro de seguridad física"),
    ("A.11", "11.2.9", "Política de escritorio limpio"),

    # A.12 Operaciones
    ("A.12", "12.1.1", "Documentación de procedimientos de operación"),
    ("A.12", "12.3.1", "Copias de seguridad (Backup)"),
    ("A.12", "12.4.1", "Registros de eventos (Logs)"),

    # A.13 Comunicaciones
    ("A.13", "13.1.1", "Controles de redes"),

    # A.14 Adquisición y Desarrollo
    ("A.14", "14.2.1", "Política de desarrollo seguro"),

    # A.15 Proveedores
    ("A.15", "15.1.1", "Política de seguridad para proveedores"),

    # A.16 Incidentes
    ("A.16", "16.1.1", "Gestión de incidentes de seguridad"),

    # A.17 Continuidad (BCP)
    ("A.17", "17.1.1", "Planificación de la continuidad"),

    # A.18 Cumplimiento
    ("A.18", "18.1.1", "Identificación de legislación aplicable"),
    ("A.18", "18.2.1", "Revisión independiente de la seguridad")
]

for norma, codigo, desc in controles_iso:
    control = ControlISO(
        codigo_norma=norma, 
        codigo_control=codigo, 
        descripcion=desc
    )
    db.add(control)

# --- 4. Crear un documento de ejemplo para que no se vea vacío ---
# (Esto ayuda a verificar que todo cargó bien)
db.commit() # Guardamos controles primero para poder relacionarlos

# Buscamos el control de políticas para asociarlo
control_politica = db.query(ControlISO).filter_by(codigo_control="5.1.1").first()

doc_ejemplo = Documento(
    titulo="Política General de Seguridad (Plantilla)",
    tipo_documento="Politica",
    version_actual="1.0",
    id_usuario_subida=admin_user.id_usuario,
    fecha_subida=datetime.utcnow(),
    proceso_asociado="Gobernanza"
)
db.add(doc_ejemplo)
db.flush()

# Relacionamos documento con el control 5.1.1
if control_politica:
    relacion = DocumentoControl(
        id_documento=doc_ejemplo.id_documento,
        id_control=control_politica.id_control,
        confirmado=True
    )
    db.add(relacion)

db.commit()
print("✅ ¡Base de datos ISO 27001 cargada correctamente!")
db.close()