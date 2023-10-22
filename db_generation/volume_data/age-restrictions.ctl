LOAD DATA
INFILE "/vol/age-restrictions.dat"
TRUNCATE
INTO TABLE AgeRestrictions
FIELDS CSV WITH EMBEDDED
TRAILING NULLCOLS
(
    age_restriction_name
)