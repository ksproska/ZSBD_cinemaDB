LOAD DATA
INFILE "/vol/shows.dat"
TRUNCATE
INTO TABLE Shows
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_show,
    start_hour,
    start_minute,
    show_date DATE "YYYY-MM-DD",
    fk_room,
    fk_movie_version
)