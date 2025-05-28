CREATE DATABASE metastore;
CREATE USER hiveuser WITH PASSWORD 'hivepassword';
GRANT ALL PRIVILEGES ON DATABASE metastore TO hiveuser;
\c metastore
CREATE SCHEMA hive;
GRANT ALL PRIVILEGES ON SCHEMA hive TO hiveuser;
ALTER SCHEMA hive OWNER TO hiveuser;
