-- Inicialización de la base de datos ISO Centro

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configuración de timezone
SET timezone = 'UTC';

-- Crear tabla de roles si no existe
CREATE TABLE IF NOT EXISTS roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Insertar roles por defecto con IDs específicos
INSERT INTO roles (id_rol, nombre_rol, descripcion) VALUES
    (1, 'Administrador', 'Acceso total al sistema'),
    (2, 'Usuario', 'Usuario estándar con acceso limitado'),
    (3, 'Auditor', 'Solo lectura para auditoría')
ON CONFLICT (id_rol) DO NOTHING;

-- Actualizar la secuencia del ID para que el próximo sea 4
SELECT setval('roles_id_rol_seq', 3, true);

-- Log de inicialización
DO $$
BEGIN
  RAISE NOTICE 'Base de datos ISO Centro inicializada correctamente';
  RAISE NOTICE 'Roles creados: Administrador, Usuario, Auditor';
END $$;
