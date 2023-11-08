-- Usuń wszystkich użytkowników, którzy nie byli na żadnym seansie od określonego czasu (np. 2 lata)
-- i nie mają żadnych aktualnych biletów (czyli takich, na które seans się jeszcze nie odbył)
-- :cutoff_date = '2024-01-17'
BEGIN
    DELETE
    FROM TICKETS
    WHERE FK_USER NOT IN (SELECT FK_USER
                          FROM TICKETS
                                   JOIN SHOWS on TICKETS.FK_SHOW = SHOWS.ID_SHOW
                          WHERE TO_DATE(:cutoff_date, 'yyyy-mm-dd') < SHOW_DATE
                            AND FK_USER IS NOT NULL GROUP BY FK_USER);
    DELETE
    FROM CINEMAUSERS
    WHERE ID_USER NOT IN (SELECT FK_USER
                          FROM TICKETS
                                   JOIN SHOWS on TICKETS.FK_SHOW = SHOWS.ID_SHOW
                          WHERE TO_DATE(:cutoff_date, 'yyyy-mm-dd') < SHOW_DATE
                            AND FK_USER IS NOT NULL);
    commit;
END;