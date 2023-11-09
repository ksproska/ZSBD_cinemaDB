UPDATE SHOWS
SET (FK_MOVIE_VERSION, SHOW_DATE) = (
    SELECT NEW_MOVIE_VERSION, NEW_SHOW_DATE
    FROM (
         SELECT
             SHOWS.ID_SHOW,
             CASE WHEN NEW_SHOW_DATE IS NOT NULL THEN NEW_SHOW_DATE ELSE SHOW_DATE END AS NEW_SHOW_DATE,
             CASE WHEN OCCUPIED_PERCENTAGE < :treshold AND ALT_MOVIE_VERSION IS NOT NULL THEN ALT_MOVIE_VERSION ELSE ID_MOVIE_VERSION END AS NEW_MOVIE_VERSION
         FROM SHOWS
                  JOIN (
             SELECT MV1.ID_MOVIE_VERSION, MIN(MV2.ID_MOVIE_VERSION) AS ALT_MOVIE_VERSION
             FROM MOVIEVERSIONS MV1 LEFT JOIN MOVIEVERSIONS MV2 ON MV1.FK_MOVIE = MV2.FK_MOVIE
             WHERE MV1.DIMENSION = '3D' AND MV2.DIMENSION <> '3D'
             GROUP BY MV1.ID_MOVIE_VERSION
         ) MOVIEVERSION_ALTERNATIVES ON FK_MOVIE_VERSION = ID_MOVIE_VERSION
                  JOIN (
             SELECT ID_SHOW,
                    SUM(CASE WHEN ID_TICKET IS NULL THEN 0 ELSE 1 END) / COUNT(*) AS OCCUPIED_PERCENTAGE
             FROM SEATS
                      JOIN ROOMS ON SEATS.FK_ROOM = ROOMS.ID_ROOM
                      JOIN SHOWS ON SHOWS.FK_ROOM = ROOMS.ID_ROOM
                      LEFT JOIN TICKETS ON TICKETS.FK_SHOW = SHOWS.ID_SHOW AND TICKETS.FK_SEAT = SEATS.ID_SEAT
             GROUP BY ID_SHOW
         ) OCCUPIED_STATS ON OCCUPIED_STATS.ID_SHOW = SHOWS.ID_SHOW
                  LEFT JOIN (
                     SELECT
                         ID_SHOW,
                         NEW_SHOW_DATE
                     FROM (
                              SELECT
                                  SHOWS.ID_SHOW,
                                  FK_ROOM,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') AS NEW_SHOW_DATE,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') AS NEW_SHOW_BEGIN,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') + NUMTODSINTERVAL(DURATION, 'MINUTE') AS NEW_SHOW_END
                              FROM SHOWS
                                       JOIN MOVIEVERSIONS ON ID_MOVIE_VERSION = FK_MOVIE_VERSION
                                       JOIN MOVIES ON FK_MOVIE = ID_MOVIE
                                       JOIN (
                                  SELECT ID_SHOW,
                                         SUM(CASE WHEN ID_TICKET IS NULL THEN 0 ELSE 1 END) / COUNT(*) AS OCCUPIED_PERCENTAGE
                                  FROM SEATS
                                           JOIN ROOMS ON SEATS.FK_ROOM = ROOMS.ID_ROOM
                                           JOIN SHOWS ON SHOWS.FK_ROOM = ROOMS.ID_ROOM
                                           LEFT JOIN TICKETS ON TICKETS.FK_SHOW = SHOWS.ID_SHOW AND TICKETS.FK_SEAT = SEATS.ID_SEAT
                                  GROUP BY ID_SHOW
                              ) OCCUPIED_STATS ON OCCUPIED_STATS.ID_SHOW = SHOWS.ID_SHOW
                              WHERE
                                      OCCUPIED_PERCENTAGE > :treshold
                                AND DIMENSION = '3D'
                          ) PROPOSED_RESCHEDULED
                     WHERE ID_SHOW NOT IN (
                        SELECT
                            PROPOSED_RESCHEDULED.ID_SHOW
                        FROM (
                        SELECT
                            SHOWS.ID_SHOW,
                                  FK_ROOM,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') AS NEW_SHOW_DATE,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') AS NEW_SHOW_BEGIN,
                                  SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') + NUMTODSINTERVAL(DURATION, 'MINUTE') AS NEW_SHOW_END
                        FROM SHOWS
                            JOIN MOVIEVERSIONS ON ID_MOVIE_VERSION = FK_MOVIE_VERSION
                            JOIN MOVIES ON FK_MOVIE = ID_MOVIE
                            JOIN (
                            SELECT ID_SHOW,
                            SUM(CASE WHEN ID_TICKET IS NULL THEN 0 ELSE 1 END) / COUNT(*) AS OCCUPIED_PERCENTAGE
                            FROM SEATS
                            JOIN ROOMS ON SEATS.FK_ROOM = ROOMS.ID_ROOM
                            JOIN SHOWS ON SHOWS.FK_ROOM = ROOMS.ID_ROOM
                            LEFT JOIN TICKETS ON TICKETS.FK_SHOW = SHOWS.ID_SHOW AND TICKETS.FK_SEAT = SEATS.ID_SEAT
                            GROUP BY ID_SHOW
                            ) OCCUPIED_STATS ON OCCUPIED_STATS.ID_SHOW = SHOWS.ID_SHOW
                        WHERE
                            OCCUPIED_PERCENTAGE > :treshold
                          AND DIMENSION = '3D'
                     ) PROPOSED_RESCHEDULED
                            JOIN SHOWS ON SHOWS.FK_ROOM = PROPOSED_RESCHEDULED.FK_ROOM
                            JOIN MOVIEVERSIONS ON FK_MOVIE_VERSION = ID_MOVIE_VERSION
                            JOIN MOVIES ON FK_MOVIE = ID_MOVIE
                        WHERE NOT (NEW_SHOW_BEGIN > SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') + NUMTODSINTERVAL(DURATION, 'MINUTE') OR SHOW_DATE + NUMTODSINTERVAL(:days_postponed,'DAY') + NUMTODSINTERVAL(START_HOUR,'HOUR') + NUMTODSINTERVAL(START_MINUTE,'MINUTE') > NEW_SHOW_END)
                    )
                 ) NONCONFLICTING ON NONCONFLICTING.ID_SHOW = SHOWS.ID_SHOW
         WHERE
                 SHOW_DATE > TO_DATE(:from_date,'yyyy-mm-dd')
        ) SHOWS_TO_SET
    WHERE SHOWS.ID_SHOW = SHOWS_TO_SET.ID_SHOW
)
WHERE
    SHOW_DATE > TO_DATE(:from_date,'yyyy-mm-dd')