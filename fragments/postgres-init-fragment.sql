-- Create database
CREATE DATABASE llc1_document_api_db;

--Create user for DB
CREATE ROLE llc1_document_api_db_user with LOGIN password 'password';

\c llc1_document_api_db;
