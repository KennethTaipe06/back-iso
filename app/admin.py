from sqladmin import Admin, ModelView
from .models import Usuario, Rol, Documento, ControlISO, DocumentoControl, HistorialVersiones

# Definimos las vistas
class UsuarioAdmin(ModelView, model=Usuario):
    column_list = [Usuario.id_usuario, Usuario.nombre_completo, Usuario.email, Usuario.rol]

class RolAdmin(ModelView, model=Rol):
    column_list = [Rol.nombre_rol, Rol.descripcion]

class DocumentoAdmin(ModelView, model=Documento):
    column_list = [Documento.titulo, Documento.version_actual, Documento.usuario_subida]

class ControlISOAdmin(ModelView, model=ControlISO):
    column_list = [ControlISO.codigo_norma, ControlISO.codigo_control]

class DocumentoControlAdmin(ModelView, model=DocumentoControl):
    column_list = [DocumentoControl.documento, DocumentoControl.control, DocumentoControl.confirmado]

class HistorialAdmin(ModelView, model=HistorialVersiones):
    column_list = [HistorialVersiones.documento, HistorialVersiones.version, HistorialVersiones.fecha_cambio]

# Función para iniciar el admin desde el main
def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(RolAdmin)
    admin.add_view(UsuarioAdmin)
    admin.add_view(ControlISOAdmin)
    admin.add_view(DocumentoAdmin)
    admin.add_view(DocumentoControlAdmin)
    admin.add_view(HistorialAdmin)