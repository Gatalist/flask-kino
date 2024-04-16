CREATE DATABASE flask_movie;
CREATE USER system76 WITH PASSWORD 'xEhs5hU26nDNdeC';
ALTER ROLE system76 SET client_encoding TO 'utf8';
ALTER ROLE system76 SET default_transaction_isolation TO 'read committed';
ALTER ROLE system76 SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE flask_movie TO system76;
GRANT ALL PRIVILEGES ON DATABASE flask_movie TO system76;

CREATE DATABASE flask_movie_test;
CREATE USER user_test WITH PASSWORD 'U26nDxEh26nDNs5';
ALTER ROLE user_test SET client_encoding TO 'utf8';
ALTER ROLE user_test SET default_transaction_isolation TO 'read committed';
ALTER ROLE user_test SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE flask_movie_test TO user_test;
GRANT ALL PRIVILEGES ON DATABASE flask_movie_test TO user_test;
