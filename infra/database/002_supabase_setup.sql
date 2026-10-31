-- Roomies PoC: setup para SQL Editor de Supabase (ejecutado como postgres).
-- Este proyecto de Supabase puede estar compartido con pruebas moviles;
-- no modifica el schema auth de Supabase ni los usuarios existentes.
--
-- En SQL Editor reemplaza TEMP_PASSWORD_AUTH y TEMP_PASSWORD_LISTADO
-- por dos contrasenas diferentes, seguras y guardadas PRIVADAMENTE.
-- NO guardes la consulta que contiene credenciales ni la subas a Git.
--
-- Nota: el rol "postgres" de Supabase no puede SET ROLE libremente a
-- nuestros roles nuevos. Por eso las tablas las crea el SQL Editor,
-- y los permisos se conceden explicitamente a cada rol de servicio.

DO $roles$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'poc_auth') THEN
        CREATE ROLE poc_auth LOGIN NOINHERIT PASSWORD 'TEMP_PASSWORD_AUTH';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'poc_listado') THEN
        CREATE ROLE poc_listado LOGIN NOINHERIT PASSWORD 'TEMP_PASSWORD_LISTADO';
    END IF;
END
$roles$;

-- Los objetos son administrados por el rol de migraciones (SQL Editor).
-- No usamos AUTHORIZATION poc_auth ni SET ROLE.
CREATE SCHEMA IF NOT EXISTS auth_users;
CREATE SCHEMA IF NOT EXISTS listado_applications;

REVOKE ALL ON SCHEMA auth_users FROM PUBLIC;
REVOKE ALL ON SCHEMA listado_applications FROM PUBLIC;
REVOKE ALL ON SCHEMA auth_users FROM poc_listado;
REVOKE ALL ON SCHEMA listado_applications FROM poc_auth;

CREATE TABLE IF NOT EXISTS auth_users.profiles (
    id UUID PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS listado_applications.publicaciones (
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

-- Ninguna de estas tablas se consulta directamente mediante
-- Supabase Data API: los servicios FastAPI acceden con sus logins SQL.
REVOKE ALL ON TABLE auth_users.profiles FROM PUBLIC;
REVOKE ALL ON TABLE listado_applications.publicaciones FROM PUBLIC;

GRANT USAGE ON SCHEMA auth_users TO poc_auth;
GRANT USAGE ON SCHEMA listado_applications TO poc_listado;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE auth_users.profiles TO poc_auth;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE listado_applications.publicaciones TO poc_listado;

-- Verificacion (en NUEVA consulta, sin contrasenas):
-- SELECT
--   has_table_privilege('poc_auth', 'auth_users.profiles', 'SELECT') AS auth_su_tabla,
--   has_table_privilege('poc_auth', 'listado_applications.publicaciones', 'SELECT') AS auth_ajena,
--   has_table_privilege('poc_listado', 'listado_applications.publicaciones', 'SELECT') AS listado_su_tabla,
--   has_table_privilege('poc_listado', 'auth_users.profiles', 'SELECT') AS listado_ajena;
-- Esperado: true, false, true, false.
