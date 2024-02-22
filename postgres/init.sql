CREATE DATABASE nix_db;
CREATE USER user_db WITH PASSWORD 'xEhs5hU26nDNdeC';
ALTER ROLE user_db SET client_encoding TO 'utf8';
ALTER ROLE user_db SET default_transaction_isolation TO 'read committed';
ALTER ROLE user_db SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE product TO user_db;