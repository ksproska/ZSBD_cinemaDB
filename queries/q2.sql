-- Wyświetl statystyki zajęcia siedzeń według filmów, czasu i typu siedzeń (VIP/normalne, połączone/pojedyńcze).
-- :year = 2023
SELECT MOVIES.NAME                                                   AS MOVIE_TITLE,
       EXTRACT(MONTH FROM SHOW_DATE)                                 AS SHOW_START_MONTH,
       START_HOUR                                                    AS SHOW_START_HOUR,
       CASE
           WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double'
           WHEN IS_VIP_SEAT = 'Y' THEN 'VIP'
           ELSE 'single' END                                         AS SEAT_TYPE,
       COUNT(ID_TICKET)                                              AS TOTAL_TICKETS_BOUGHT,
       COUNT(ID_TICKET) / COUNT(DISTINCT ID_SHOW)                    AS AVERAGE_TICKETS_PER_SHOW,
       SUM(CASE WHEN ID_TICKET IS NULL THEN 0 ELSE 1 END) / COUNT(*) AS OCCUPIED_PERCENTAGE
FROM SEATS
         JOIN ROOMS ON SEATS.FK_ROOM = ROOMS.ID_ROOM
         JOIN SHOWS ON SHOWS.FK_ROOM = ROOMS.ID_ROOM
         JOIN MOVIEVERSIONS ON SHOWS.FK_MOVIE_VERSION = MOVIEVERSIONS.ID_MOVIE_VERSION
         JOIN MOVIES ON MOVIEVERSIONS.FK_MOVIE = MOVIES.ID_MOVIE
         LEFT JOIN TICKETS ON TICKETS.FK_SHOW = SHOWS.ID_SHOW
WHERE EXTRACT(YEAR FROM SHOW_DATE) = '&1'
  AND TICKETS.FK_SEAT = SEATS.ID_SEAT
GROUP BY MOVIES.NAME, EXTRACT(MONTH FROM SHOW_DATE), START_HOUR,
         CASE WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double' WHEN IS_VIP_SEAT = 'Y' THEN 'VIP' ELSE 'single' END
ORDER BY MOVIES.Name, SHOW_START_MONTH, TOTAL_TICKETS_BOUGHT;
