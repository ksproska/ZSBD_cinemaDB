select LAST_LOAD_TIME, ELAPSED_TIME, MODULE, SQL_TEXT elapsed from v$sql
  order by LAST_LOAD_TIME desc;
select count(*) from Tickets;