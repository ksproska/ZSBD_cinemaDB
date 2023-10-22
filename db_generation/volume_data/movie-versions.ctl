LOAD DATA
INFILE "/vol/movie-versions.dat"
TRUNCATE
INTO TABLE MovieVersions
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(id_movie_version, dimension, fk_dubbing_language, fk_subtitles_language, fk_voice_over_language, fk_movie)