spool /vol/res.txt;
set timing on;
select NAME, PREMIERE from MOVIES where PREMIERE > to_date(2018, 'YYYY');
select SPONSOR from ROOMS where CAPABLE_3D = 'Y';
select BASE_PRICE, DISCOUNT, BASE_PRICE * (1 - TICKETS.DISCOUNT) from TICKETS where FK_SHOW = 11;