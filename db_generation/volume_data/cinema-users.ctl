LOAD DATA
INFILE "/vol/cinema-users.dat"
TRUNCATE
INTO TABLE CinemaUsers
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_user,
    name,
    surname,
    email,
    password,
    birth DATE "YYYY-MM-DD"
)