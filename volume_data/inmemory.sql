ALTER TABLE tickets INMEMORY MEMCOMPRESS FOR QUERY LOW
  NO INMEMORY (purchase);

ALTER TABLE shows INMEMORY MEMCOMPRESS FOR QUERY LOW;

ALTER TABLE seats INMEMORY MEMCOMPRESS FOR QUERY LOW;

ALTER TABLE rooms INMEMORY MEMCOMPRESS FOR QUERY LOW
  NO INMEMORY (wheelchair_avability, sponsor);

ALTER TABLE movies INMEMORY MEMCOMPRESS FOR QUERY LOW
  NO INMEMORY (premiere, description, fk_age_restriction);

ALTER TABLE MovieVersions INMEMORY MEMCOMPRESS FOR QUERY LOW;

ALTER TABLE CinemaUsers INMEMORY MEMCOMPRESS FOR QUERY LOW
  NO INMEMORY (name, surname, email, password, birth);

ALTER TABLE languages INMEMORY MEMCOMPRESS FOR QUERY LOW;