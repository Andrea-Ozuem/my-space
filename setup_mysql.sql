-- Prepares a MySQL server for the project.
CREATE DATABASE IF NOT EXISTS space_db;
CREATE USER IF NOT EXISTS 'andrea'@'localhost' IDENTIFIED BY 'andrea';
GRANT ALL PRIVILEGES ON space_db . * TO 'andrea'@'localhost';
GRANT SELECT ON performance_schema . * TO 'andrea'@'localhost';
