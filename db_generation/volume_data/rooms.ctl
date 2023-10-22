LOAD DATA
INFILE "/vol/rooms.dat"
TRUNCATE
INTO TABLE rooms
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_room,
    room_sign,
    floor_number,
    imax_capable,
    wheelchair_availability,
    sponsor,
    capable_3D
)