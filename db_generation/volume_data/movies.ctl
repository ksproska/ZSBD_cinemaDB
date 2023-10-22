LOAD DATA
INFILE "/vol/movies.dat"
TRUNCATE
INTO TABLE Movies
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_movie,
    name,
    premiere DATE "YYYY-MM-DD",
    duration,
    is_imax,
    fk_language,
    fk_age_restriction
)