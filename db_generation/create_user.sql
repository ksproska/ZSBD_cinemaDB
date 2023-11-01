create user test identified by test;
grant connect, resource to test;
grant unlimited tablespace to test;
CREATE OR REPLACE DIRECTORY "DATA_PUMP_DIR" as '/vol';