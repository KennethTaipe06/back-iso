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

-- Insertar roles por defecto
INSERT INTO roles (nombre_rol, descripcion) VALUES
    ('Administrador', 'Acceso total al sistema'),
    ('Usuario', 'Usuario estándar con acceso limitado'),
    ('Auditor', 'Solo lectura para auditoría')
ON CONFLICT (nombre_rol) DO NOTHING;

-- Log de inicialización
DO $$
BEGIN
  RAISE NOTICE 'Base de datos ISO Centro inicializada correctamente';
  RAISE NOTICE 'Roles creados: Administrador, Usuario, Auditor';
END $$;
