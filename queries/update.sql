-- Przenieś wszystkie seanse w określonym okresie z danej sali kinowej do innych sal kinowych o wymaganym wyposażeniu
-- (dla filmu 3D sala musi udostępniać 3D, dla IMAX musi udostępniać IMAX) tak, żeby zachować miejsca VIP i podwójne
-- (dla biletów wykupionych na miejscach VIP nowo przypisane miejsce również musi być VIP), chyba że nie jest to możliwe.
-- :start_time = TIMESTAMP '2023-07-25 8:00:00' :end_time = TIMESTAMP '2023-07-25 23:00:00' :room_number = 1
SELECT DISTINCT ID_SHOW,
--        ID_MOVIE,
--        SHOWS_TO_MOVE.DURATION AS MOVIE_DURATION,
       EMPTY_SLOTS.START_TIME          AS EMPTY_SLOT_START_TIME,
       EMPTY_SLOTS.ID_ROOM             AS NEW_ROOM_ID,
       EMPTY_SLOTS.BREAK_BETWEEN_SHOWS AS EMPTY_SLOT_DURATION
--        SHOWS_TO_MOVE.TOTAL_TICKETS,
--        EMPTY_SLOTS.TOTAL_TICKETS,
--        SHOWS_TO_MOVE.IS_VIP_SEAT,
--        EMPTY_SLOTS.IS_VIP_SEAT,
--        SHOWS_TO_MOVE.IS_CONNECTED_SEAT,
--        EMPTY_SLOTS.IS_CONNECTED_SEAT,
--        SHOWS_TO_MOVE.DIMENSION,
--        SHOWS_TO_MOVE.IS_IMAX,
FROM (SELECT ID_SHOW,
             ID_MOVIE,
--        SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') + NUMTODSINTERVAL(START_MINUTE, 'MINUTE') AS START_TIME,
             DURATION,
             MV.DIMENSION,
             M.IS_IMAX                                                 AS IS_IMAX,
             COUNT(*)                                                  AS TOTAL_TICKETS,
             IS_VIP_SEAT,
             CASE WHEN FK_CONNECTED_SEAT IS NULL THEN 'N' ELSE 'Y' END AS IS_CONNECTED_SEAT
      FROM SHOWS
               JOIN MOVIEVERSIONS MV on MV.ID_MOVIE_VERSION = SHOWS.FK_MOVIE_VERSION
               JOIN MOVIES M on MV.FK_MOVIE = M.ID_MOVIE
               JOIN TICKETS T on SHOWS.ID_SHOW = T.FK_SHOW
               JOIN SEATS S on T.FK_SEAT = S.ID_SEAT
      WHERE :start_time <= SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') + NUMTODSINTERVAL(START_MINUTE, 'MINUTE')
        AND SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') + NUMTODSINTERVAL(START_MINUTE, 'MINUTE') +
            NUMTODSINTERVAL(DURATION, 'MINUTE') <= :end_time
        AND S.FK_ROOM = :room_number
      group by ID_SHOW,
               SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') + NUMTODSINTERVAL(START_MINUTE, 'MINUTE'),
               ID_MOVIE,
               DURATION,
               MV.DIMENSION,
               IS_IMAX,
               IS_VIP_SEAT,
               CASE WHEN FK_CONNECTED_SEAT IS NULL THEN 'N' ELSE 'Y' END) SHOWS_TO_MOVE,

     (WITH SHOWS_TIMES AS (SELECT ID_SHOW,
                                  FK_ROOM                                 AS ID_ROOM,
                                  SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                  NUMTODSINTERVAL(START_MINUTE, 'MINUTE') AS START_TIME,
                                  SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                  NUMTODSINTERVAL(START_MINUTE, 'MINUTE') +
                                  NUMTODSINTERVAL(DURATION, 'MINUTE')     AS END_TIME
                           FROM SHOWS S
                                    JOIN MOVIEVERSIONS MV on MV.ID_MOVIE_VERSION = S.FK_MOVIE_VERSION
                                    JOIN MOVIES M on MV.FK_MOVIE = M.ID_MOVIE
                           WHERE :start_time <=
                                 SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                 NUMTODSINTERVAL(START_MINUTE, 'MINUTE')
                             AND SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                 NUMTODSINTERVAL(START_MINUTE, 'MINUTE') +
                                 NUMTODSINTERVAL(DURATION, 'MINUTE') <= :end_time),
           ROOMS_INTERVALS AS (SELECT ST1.ID_ROOM,
                                      ST1.END_TIME                                               AS START_TIME,
                                      NUMTODSINTERVAL(MIN(ST2.START_TIME - ST1.END_TIME), 'DAY') AS BREAK_BETWEEN_SHOWS
                               FROM SHOWS_TIMES ST1
                                        JOIN SHOWS_TIMES ST2 ON ST1.ID_ROOM = ST2.ID_ROOM
                               WHERE ST1.ID_SHOW != ST2.ID_SHOW
                                 AND ST1.END_TIME < ST2.START_TIME
                               GROUP BY ST1.ID_ROOM, ST2.START_TIME, ST1.END_TIME),
           ROOM_INTERVALS_AND_CAPASITY AS (SELECT ID_ROOM,
                                                  START_TIME,
                                                  MIN(BREAK_BETWEEN_SHOWS)                                  AS BREAK_BETWEEN_SHOWS,
                                                  COUNT(*)                                                  AS TOTAL_TICKETS,
                                                  IS_VIP_SEAT,
                                                  CASE WHEN FK_CONNECTED_SEAT IS NULL THEN 'N' ELSE 'Y' END AS IS_CONNECTED_SEAT
                                           FROM ROOMS_INTERVALS
                                                    JOIN SEATS ON ID_ROOM = FK_ROOM
                                           WHERE ID_ROOM != :room_number
                                           GROUP BY ID_ROOM, START_TIME, IS_VIP_SEAT,
                                                    CASE WHEN FK_CONNECTED_SEAT IS NULL THEN 'N' ELSE 'Y' END)
      SELECT *
      FROM ROOM_INTERVALS_AND_CAPASITY
      ORDER BY ID_ROOM, START_TIME) EMPTY_SLOTS
         JOIN ROOMS ON EMPTY_SLOTS.ID_ROOM = ROOMS.ID_ROOM
WHERE NUMTODSINTERVAL(SHOWS_TO_MOVE.DURATION, 'MINUTE') < EMPTY_SLOTS.BREAK_BETWEEN_SHOWS
  AND SHOWS_TO_MOVE.IS_IMAX = ROOMS.IMAX_CAPABLE
  AND (SHOWS_TO_MOVE.DIMENSION = '2D' OR ROOMS.CAPABLE_3D = 'Y')
  AND SHOWS_TO_MOVE.IS_VIP_SEAT = EMPTY_SLOTS.IS_VIP_SEAT
  AND SHOWS_TO_MOVE.IS_CONNECTED_SEAT = EMPTY_SLOTS.IS_CONNECTED_SEAT
  AND SHOWS_TO_MOVE.TOTAL_TICKETS <= EMPTY_SLOTS.TOTAL_TICKETS
ORDER BY ID_SHOW, EMPTY_SLOT_START_TIME, NEW_ROOM_ID;