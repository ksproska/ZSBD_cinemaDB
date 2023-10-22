LOAD DATA
INFILE "/vol/tickets.dat"
TRUNCATE
INTO TABLE Tickets
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_ticket,
    discount,
    base_price,
    purchase TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
    fk_seat,
    fk_show,
    fk_user
)