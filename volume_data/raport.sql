alter system flush buffer_cache;
alter system flush shared_pool;
alter session set current_schema = TEST;
set linesize 150
spool /vol/res.txt;
@@/vol/q1.sql '2023-07-25' 8 0 600;
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/q2.sql 2023;
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/q3.sql;
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/q4.sql 10 'The Godfather' '2023-07-24 8:00:00' '2023-12-30 20:44:00';
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/update.sql 95 300 '2023-12-30';
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/pre-insert.sql 15876;
@@/vol/insert.sql 15876;
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
@@/vol/delete2.sql '2024-01-10';
select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
select * from movies;
rollback;
-- alter system flush buffer_cache;
-- alter system flush shared_pool;
-- create index timestamp_ix on SHOWS (SHOW_DATE + numtodsinterval(START_HOUR, 'HOUR') +
--                                     numtodsinterval(START_MINUTE, 'MINUTE'));
-- CREATE INDEX shows_year ON SHOWS (EXTRACT(YEAR FROM SHOW_DATE));
-- CREATE INDEX tickets_fk_show ON TICKETS(FK_SHOW, BASE_PRICE, DISCOUNT);
-- CREATE INDEX tickets_fks_seats_shows ON TICKETS (FK_SEAT, FK_SHOW);
-- CREATE BITMAP INDEX rooms_capabilities ON ROOMS(IMAX_CAPABLE, CAPABLE_3D);
-- @@/vol/pre-insert.sql 15876;
-- @@/vol/insert.sql 15876;
-- select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
-- @@/vol/delete2.sql '2024-01-10';
-- select * from table ( DBMS_XPLAN.DISPLAY_CURSOR );
-- rollback;