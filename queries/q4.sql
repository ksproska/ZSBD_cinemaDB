-- Pokaż sale, w których można zaplanować projekcję danego filmu dla zadanej liczby osób i danego tytułu w zadanym przedziale czasowym
-- :required_seats = 10 :movie_name = 'The Godfather' :start_timestamp = TIMESTAMP '2023-07-24 8:00:00' :end_timestamp = TIMESTAMP '2023-12-30 20:44:00'
WITH ROOM_CAPACITY AS (SELECT ID_ROOM, ROOM_SIGN, IMAX_CAPABLE, CAPABLE_3D
                       FROM ROOMS
                                JOIN SEATS ON ROOMS.ID_ROOM = SEATS.FK_ROOM
                       GROUP BY ID_ROOM, ROOM_SIGN, IMAX_CAPABLE, CAPABLE_3D
                       HAVING COUNT(DISTINCT ID_SEAT) > :required_seats),
     AVAILABLE_MOVIE_VERSIONS AS (SELECT NAME AS MOVIE_TITLE, DURATION, IS_IMAX, M.DIMENSION
                                  FROM MOVIES
                                           JOIN MOVIEVERSIONS M on MOVIES.ID_MOVIE = M.FK_MOVIE
                                  WHERE MOVIES.NAME = :movie_name),
     CAPABLE_ROOMS_FOR_MOVIE AS (SELECT DISTINCT ID_ROOM, ROOM_SIGN, DURATION
                                 FROM AVAILABLE_MOVIE_VERSIONS,
                                      ROOM_CAPACITY
                                 WHERE AVAILABLE_MOVIE_VERSIONS.IS_IMAX = ROOM_CAPACITY.IMAX_CAPABLE
                                   AND (AVAILABLE_MOVIE_VERSIONS.DIMENSION = '2D' OR
                                        (AVAILABLE_MOVIE_VERSIONS.DIMENSION = '3D' AND
                                         ROOM_CAPACITY.CAPABLE_3D = 'Y'))),
     SHOWS_START_END_TIMESTAMPS AS (SELECT ID_SHOW,
                                           FK_ROOM                                 AS ROOM_ID,
                                           SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                           NUMTODSINTERVAL(START_MINUTE, 'MINUTE') AS START_DATE,
                                           SHOW_DATE + NUMTODSINTERVAL(START_HOUR, 'HOUR') +
                                           NUMTODSINTERVAL(START_MINUTE, 'MINUTE') +
                                           NUMTODSINTERVAL(M3.DURATION, 'MINUTE')  AS END_DATE,
                                           NUMTODSINTERVAL(M3.DURATION, 'MINUTE')  AS DURATION
                                    FROM SHOWS
                                             JOIN MOVIEVERSIONS M2 on SHOWS.FK_MOVIE_VERSION = M2.ID_MOVIE_VERSION
                                             JOIN MOVIES M3 on M2.FK_MOVIE = M3.ID_MOVIE,
                                         CAPABLE_ROOMS_FOR_MOVIE
                                    WHERE FK_ROOM IN CAPABLE_ROOMS_FOR_MOVIE.ID_ROOM),
     SHOWS_START_END_TIMESTAMPS_FOR_DATES AS (SELECT ID_SHOW,
                                                     ROOM_ID,
                                                     START_DATE,
                                                     END_DATE,
                                                     DURATION
                                              FROM SHOWS_START_END_TIMESTAMPS
                                              WHERE END_DATE >= :start_timestamp
                                                AND START_DATE <= :end_timestamp),
     SHOW_INTERVALS AS (SELECT RS1.ROOM_ID,
                               RS1.END_DATE                                               AS BEGIN_TIME,
                               NUMTODSINTERVAL(MIN(RS2.START_DATE - RS1.END_DATE), 'DAY') AS BREAK_BETWEEN_SHOWS
                        FROM SHOWS_START_END_TIMESTAMPS_FOR_DATES RS1
                                 JOIN SHOWS_START_END_TIMESTAMPS_FOR_DATES RS2 ON RS1.ROOM_ID = RS2.ROOM_ID
                        WHERE RS1.END_DATE < RS2.START_DATE
                          AND RS1.ROOM_ID = RS2.ROOM_ID
                        GROUP BY RS1.ROOM_ID, RS1.END_DATE, RS1.DURATION)
SELECT ROOM_ID,
       BEGIN_TIME,
       BREAK_BETWEEN_SHOWS,
       BREAK_BETWEEN_SHOWS - NUMTODSINTERVAL(DURATION, 'MINUTE') AS EXTRA_TIME
FROM SHOW_INTERVALS
         JOIN CAPABLE_ROOMS_FOR_MOVIE ON SHOW_INTERVALS.ROOM_ID = CAPABLE_ROOMS_FOR_MOVIE.ID_ROOM
WHERE BREAK_BETWEEN_SHOWS >= NUMTODSINTERVAL(DURATION, 'MINUTE')
ORDER BY ROOM_ID, BEGIN_TIME;
