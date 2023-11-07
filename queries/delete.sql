-- Usuń wszystkich użytkowników, którzy nie byli na żadnym seansie od określonego czasu (np. 2 lata)
-- i nie mają żadnych aktualnych biletów (czyli takich, na które seans się jeszcze nie odbył)
-- :cutoff_date = '2023-08-01'
DELETE
FROM CINEMAUSERS
WHERE ID_USER NOT IN (SELECT FK_USER
                      FROM TICKETS
                               JOIN SHOWS S on TICKETS.FK_SHOW = S.ID_SHOW
                      WHERE SHOW_DATE < TO_DATE(:cutoff_date, 'yyyy-mm-dd')
                        AND FK_USER IS NOT NULL);
