-- Grupie z ostatniego seansu bardzo się spodobało siedzenie we własnym towarzystwie, więc postanowili sobie zarezerwować
-- w najbliższym dostępnym terminie maraton śmierci: wszystkie filmy, jakie da się w tej sali wyświetlić po kolei,
-- w dowolnej wersji językowej.
-- :selected_show = 15876

INSERT INTO TICKETS SELECT LAST_ID_TICKET + ROWNUM AS ID_TICKET,
       DISCOUNT,
       BASE_PRICE,
       CURRENT_TIMESTAMP AS PURCHASE,
       FK_SEAT,
       ID_SHOW AS FK_SHOW,
       FK_USER
FROM TICKETS,
     (SELECT ID_TICKET AS LAST_ID_TICKET
      FROM (SELECT ID_TICKET FROM TICKETS ORDER BY ID_TICKET DESC)
      WHERE ROWNUM <= 1), (SELECT ID_SHOW
FROM (SELECT COUNT(*) AS NUMB_OF_SHOWS_INSERTED
      FROM (SELECT MIN(MV.ID_MOVIE_VERSION) AS ID_MOVIE_VERSION,
                   M.ID_MOVIE,
                   M.DURATION
            FROM SHOWS
                     JOIN ROOMS R ON R.ID_ROOM = SHOWS.FK_ROOM,
                 MOVIEVERSIONS MV
                     JOIN MOVIES M on MV.FK_MOVIE = M.ID_MOVIE
            WHERE ID_SHOW = '&1'
              AND IMAX_CAPABLE = IS_IMAX
              AND (DIMENSION = '2D' OR DIMENSION = '3D' AND CAPABLE_3D = 'Y')
            group by M.DURATION, M.ID_MOVIE)),
     (SELECT ID_SHOW AS LAST_ID_SHOW FROM (SELECT ID_SHOW FROM SHOWS ORDER BY ID_SHOW DESC) WHERE ROWNUM <= 1),
     SHOWS
WHERE SHOWS.ID_SHOW > LAST_ID_SHOW - NUMB_OF_SHOWS_INSERTED)
WHERE FK_SHOW = '&1';
