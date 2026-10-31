-- SOLO DESARROLLO: contraseñas conocidas para PostgreSQL de Docker Compose.
-- NUNCA utilizar estas credenciales en Supabase ni en producción.
CREATE ROLE poc_auth LOGIN PASSWORD 'solo_local_auth';
CREATE ROLE poc_listado LOGIN PASSWORD 'solo_local_listado';

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
