-- Grupie z ostatniego seansu bardzo się spodobało siedzenie we własnym towarzystwie, więc postanowili sobie zarezerwować
-- w najbliższym dostępnym terminie maraton śmierci: wszystkie filmy, jakie da się w tej sali wyświetlić po kolei,
-- w dowolnej wersji językowej.
-- :selected_show = 6

INSERT INTO SHOWS (ID_SHOW, SHOW_DATE, START_HOUR, START_MINUTE, FK_ROOM, FK_MOVIE_VERSION)
WITH MOVIE_VERSIONS_FOR_ROOM AS (
-- all movie versions with durations
    SELECT MIN(MV.ID_MOVIE_VERSION) AS ID_MOVIE_VERSION,
           M.ID_MOVIE,
           M.DURATION
--        M.PREMIERE
    FROM SHOWS
             JOIN ROOMS R ON R.ID_ROOM = SHOWS.FK_ROOM,
         MOVIEVERSIONS MV
             JOIN MOVIES M on MV.FK_MOVIE = M.ID_MOVIE
    WHERE ID_SHOW = :selected_show
      AND IMAX_CAPABLE = IS_IMAX
      AND (DIMENSION = '2D' OR DIMENSION = '3D' AND CAPABLE_3D = 'Y')
    group by M.DURATION, M.ID_MOVIE),
     LAST_SHOW_END AS
-- LAST_SHOW_END_TIME
         (SELECT *
          FROM (SELECT S.SHOW_DATE + NUMTODSINTERVAL(S.START_HOUR, 'HOUR') +
                       NUMTODSINTERVAL(S.START_MINUTE, 'MINUTE') +
                       NUMTODSINTERVAL(M.DURATION, 'MINUTE') AS LAST_SHOW_END_TIME
                FROM SHOWS SS,
                     SHOWS S
                         JOIN MOVIEVERSIONS MV on MV.ID_MOVIE_VERSION = S.FK_MOVIE_VERSION
                         JOIN MOVIES M on MV.FK_MOVIE = M.ID_MOVIE
                WHERE SS.ID_SHOW = :selected_show
                  AND SS.FK_ROOM = S.FK_ROOM
                ORDER BY LAST_SHOW_END_TIME DESC)
          WHERE ROWNUM <= 1),
     TEMP AS (SELECT ID_MOVIE_VERSION,
                     DURATION,
                     LAST_SHOW_END_TIME,
                     ROWNUM
              FROM MOVIE_VERSIONS_FOR_ROOM,
                   LAST_SHOW_END)
SELECT
    T2."ROWNUM" + 30000 AS ID_SHOW,
--     T2.LAST_SHOW_END_TIME + NUMTODSINTERVAL((T2."ROWNUM" - 1) * MAX(TEMP.DURATION), 'MINUTE') AS NEW_START_TIME,
    TO_DATE(TRUNC(T2.LAST_SHOW_END_TIME + NUMTODSINTERVAL((T2."ROWNUM" - 1) * MAX(TEMP.DURATION), 'MINUTE'))) AS SHOW_DATE,
    TO_NUMBER(TO_CHAR(T2.LAST_SHOW_END_TIME + NUMTODSINTERVAL((T2."ROWNUM" - 1) * MAX(TEMP.DURATION), 'MINUTE'), 'HH24')) AS START_HOUR,
    TO_NUMBER(TO_CHAR(T2.LAST_SHOW_END_TIME + NUMTODSINTERVAL((T2."ROWNUM" - 1) * MAX(TEMP.DURATION), 'MINUTE'), 'MI')) AS START_MINUTE,
--     T2.LAST_SHOW_END_TIME + NUMTODSINTERVAL(T2."ROWNUM" * MAX(TEMP.DURATION), 'MINUTE') AS NEW_END_TIME,
    FK_ROOM,
    T2.ID_MOVIE_VERSION AS FK_MOVIE_VERSION
FROM TEMP, TEMP T2, SHOWS WHERE ID_SHOW = :selected_show
group by T2.ID_MOVIE_VERSION, T2.DURATION, T2.LAST_SHOW_END_TIME, T2."ROWNUM", FK_ROOM
ORDER BY T2."ROWNUM";
