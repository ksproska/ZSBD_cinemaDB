LOAD DATA
INFILE "/vol/languages.dat"
TRUNCATE
INTO TABLE Languages
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    id_language,
    language_name
)