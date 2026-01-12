-- Inicialización de la base de datos ISO Centro

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios (se creará automáticamente por SQLAlchemy)
-- Este archivo es para datos iniciales o configuración extra

-- Datos de ejemplo (opcional)
-- INSERT INTO usuarios (username, email, hashed_password, is_active, is_admin) 
-- VALUES ('admin', 'admin@iso.com', 'hash_aqui', true, true);

-- Configuración de timezone
SET timezone = 'UTC';

-- Log de inicialización
DO $$
BEGIN
  RAISE NOTICE 'Base de datos ISO Centro inicializada correctamente';
END $$;
