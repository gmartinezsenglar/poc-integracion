-- Ejecutar en Supabase SQL Editor de un proyecto EXCLUSIVO de pruebas.
-- NO pegar contraseñas reales en archivos de Git ni reutilizar contraseñas locales.
-- 1. Reemplazar los dos marcadores TEMP_PASSWORD_AUTH y TEMP_PASSWORD_LISTADO
--    por contraseñas diferentes, largas y aleatorias antes de ejecutar.
-- 2. Guardar cada contraseña en el gestor de secretos y configurar su DATABASE_URL.
-- 3. No dar a estos roles permisos sobre auth.*, storage.* ni esquema ajeno.
CREATE ROLE poc_auth LOGIN PASSWORD 'TEMP_PASSWORD_AUTH';
CREATE ROLE poc_listado LOGIN PASSWORD 'TEMP_PASSWORD_LISTADO';

CREATE SCHEMA auth_users AUTHORIZATION poc_auth;
CREATE SCHEMA listado_applications AUTHORIZATION poc_listado;
REVOKE ALL ON SCHEMA auth_users FROM PUBLIC;
REVOKE ALL ON SCHEMA listado_applications FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM poc_auth, poc_listado;

SET ROLE poc_auth;
CREATE TABLE auth_users.profiles (
    id UUID PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
RESET ROLE;

SET ROLE poc_listado;
CREATE TABLE listado_applications.publicaciones (
    id UUID PRIMARY KEY,
    autor_id UUID NOT NULL,
    titulo VARCHAR(140) NOT NULL,
    region VARCHAR(100) NOT NULL,
    comuna VARCHAR(100) NOT NULL,
    precio_clp INTEGER NOT NULL CHECK (precio_clp > 0),
    cupos_totales INTEGER NOT NULL CHECK (cupos_totales BETWEEN 1 AND 20),
    tipo VARCHAR(20) NOT NULL DEFAULT 'Compartida',
    estado VARCHAR(20) NOT NULL DEFAULT 'Disponible',
    fecha_publicacion TIMESTAMPTZ NOT NULL DEFAULT now()
);
RESET ROLE;

-- Comprobar aislamiento en consultas separadas, conectando como poc_auth:
-- SELECT * FROM auth_users.profiles LIMIT 1;                -- PERMITIDO
-- SELECT * FROM listado_applications.publicaciones LIMIT 1; -- DENEGADO
-- Y como poc_listado:
-- SELECT * FROM listado_applications.publicaciones LIMIT 1; -- PERMITIDO
-- SELECT * FROM auth_users.profiles LIMIT 1;                 -- DENEGADO
