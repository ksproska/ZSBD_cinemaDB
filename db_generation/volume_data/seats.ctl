LOAD DATA
INFILE "/vol/seats.dat"
TRUNCATE
INTO TABLE Seats
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_seat,
    seat_row,
    seat_number,
    is_vip_seat,
    fk_room,
    fk_connected_seat
)