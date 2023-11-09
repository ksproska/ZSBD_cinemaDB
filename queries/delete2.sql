DELETE
    FROM TICKETS
    WHERE ID_TICKET IN (
        SELECT ID_TICKET
        FROM TICKETS
            JOIN SHOWS on TICKETS.FK_SHOW = SHOWS.ID_SHOW
        WHERE TO_DATE(:date, 'yyyy-mm-dd') < SHOW_DATE
    );