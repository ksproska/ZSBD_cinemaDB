SELECT MOVIES.NAME, EXTRACT(MONTH FROM SHOW_DATE) AS MONTH, START_HOUR,
       CASE WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double' WHEN IS_VIP_SEAT = 'Y' THEN 'VIP' ELSE 'single' END AS SEAT_TYPE,
       COUNT(ID_TICKET) AS TOTAL_TICKETS_BOUGHT,
       COUNT(ID_TICKET)/COUNT(DISTINCT ID_SHOW) AS AVERAGE_TICKETS_PER_SHOW,
       SUM(CASE WHEN ID_TICKET IS NULL THEN 0 ELSE 1 END)/COUNT(*) AS OCCUPIED_PERCENTAGE
FROM SEATS, ROOMS, SHOWS, MOVIEVERSIONS, MOVIES
    LEFT JOIN TICKETS T ON FK_SHOW
WHERE
    EXTRACT(YEAR FROM SHOW_DATE) = :year
    AND T.FK_SHOW = ID_SHOW
GROUP BY MOVIES.NAME, EXTRACT(MONTH FROM SHOW_DATE), START_HOUR, CASE WHEN FK_CONNECTED_SEAT IS NOT NULL THEN 'double' WHEN IS_VIP_SEAT = 'Y' THEN 'VIP' ELSE 'single' END
ORDER BY MOVIES.Name, MONTH;
