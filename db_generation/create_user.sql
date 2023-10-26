create user test identified by test;
grant connect, resource to test;
grant unlimited tablespace to test;
CREATE OR REPLACE DIRECTORY "DATA_PUMP_DIR" as '/vol';
SELECT owner, directory_name, directory_path FROM dba_directories WHERE directory_name='DATA_PUMP_DIR';