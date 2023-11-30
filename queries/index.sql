create index timestamp_ix on SHOWS (SHOW_DATE + numtodsinterval(START_HOUR, 'HOUR') +
                                    numtodsinterval(START_MINUTE, 'MINUTE'));
CREATE INDEX shows_year ON SHOWS (EXTRACT(YEAR FROM SHOW_DATE));
CREATE INDEX tickets_fk_show ON TICKETS(FK_SHOW, BASE_PRICE, DISCOUNT);
CREATE INDEX tickets_fks_seats_shows ON TICKETS (FK_SEAT, FK_SHOW);
CREATE BITMAP INDEX rooms_capabilities ON ROOMS(IMAX_CAPABLE, CAPABLE_3D);

CREATE INDEX movie_dimension ON MOVIEVERSIONS(DIMENSION);
CREATE BITMAP INDEX shows_year ON SHOWS (EXTRACT(YEAR FROM SHOW_DATE));
CREATE INDEX tickets_fk_show ON TICKETS(FK_SHOW, BASE_PRICE * (1 - DISCOUNT), BASE_PRICE * DISCOUNT);
CREATE INDEX tickets_fk_seat ON TICKETS (FK_SEAT);
CREATE INDEX tickets_fk_show ON TICKETS (FK_SHOW);
CREATE INDEX shows_fk_room ON SHOWS (FK_ROOM);
CREATE INDEX seats_fk_room ON SEATS (FK_ROOM);
CREATE BITMAP INDEX rooms_imax ON ROOMS(IMAX_CAPABLE);
CREATE BITMAP INDEX movies_imax ON MOVIES(IS_IMAX);
CREATE INDEX seats_stats ON SEATS(ID_SEAT, FK_ROOM, CASE WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double' WHEN IS_VIP_SEAT = 'Y' THEN 'VIP' ELSE 'single' END);
CREATE INDEX seats_stats ON SEATS(FK_ROOM, ID_SEAT, CASE WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double' WHEN IS_VIP_SEAT = 'Y' THEN 'VIP' ELSE 'single' END);

DROP index timestamp_ix;
DROP INDEX shows_year;
DROP INDEX tickets_fk_show;
drop index tickets_fks_seats_shows;
drop index rooms_capabilities;

drop index movie_dimension;
DROP INDEX shows_fk_room;
DROP INDEX seats_fk_room;
DROP INDEX tickets_fk_seat;
drop index movies_imax;
drop index rooms_imax;
drop index tickets_fk_show;
drop index seats_stats;