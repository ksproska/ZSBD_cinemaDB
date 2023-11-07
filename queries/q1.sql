-- Wyświetl wszystkie wolne miejsca na seanse
-- rozpoczynające się w od danej godziny i minuty do max zadanego przedziału w godzinach
WITH SELECTED_SHOWS(ID_SHOW, ID_ROOM, START_TIME, ID_SEAT, SEAT_ROW, SEAT_NUMBER, IS_VIP_SEAT, IS_DOUBLE_SEAT, ID_TICKET)
         AS (SELECT ID_SHOW                                                           AS ID_SHOW,
                    ID_ROOM,
                    SHOWS.SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                    NUMTODSINTERVAL(START_MINUTE, 'MINUTE')                           AS START_TIME,
                    ID_SEAT,
                    SEAT_ROW,
                    SEAT_NUMBER,
                    IS_VIP_SEAT,
                    (CASE WHEN (FK_CONNECTED_SEAT IS NOT NULL) THEN 'Y' ELSE 'N' END) AS IS_DOUBLE_SEAT,
                    ID_TICKET
             FROM SHOWS
                      JOIN ROOMS on ROOMS.ID_ROOM = SHOWS.FK_ROOM
                      JOIN SEATS S on ROOMS.ID_ROOM = S.FK_ROOM
                      LEFT JOIN TICKETS on S.ID_SEAT = TICKETS.FK_SEAT AND SHOWS.ID_SHOW = TICKETS.FK_SHOW
             WHERE TO_DATE(:show_date, 'yyyy-mm-dd') + NUMTODSINTERVAL(:start_hour, 'HOUR') +
                   NUMTODSINTERVAL(:start_minutes, 'MINUTE') <=
                   SHOWS.SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                   NUMTODSINTERVAL(START_MINUTE, 'MINUTE')
               AND TO_DATE(:show_date, 'yyyy-mm-dd') + NUMTODSINTERVAL(:start_hour, 'HOUR') +
                   NUMTODSINTERVAL(:start_minutes, 'MINUTE') +
                   NUMTODSINTERVAL(:seek_length_hours, 'HOUR') >=
                   SHOWS.SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                   NUMTODSINTERVAL(START_MINUTE, 'MINUTE')
             ORDER BY START_TIME, ID_SHOW, SEAT_ROW, SEAT_NUMBER)
SELECT ID_SHOW,
       START_TIME,
       SEAT_ROW,
       SEAT_NUMBER,
       IS_VIP_SEAT,
       IS_DOUBLE_SEAT
FROM SELECTED_SHOWS
WHERE ID_TICKET IS NOT NULL
ORDER BY START_TIME, ID_SHOW, SEAT_ROW, SEAT_NUMBER;
