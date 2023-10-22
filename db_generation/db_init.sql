-- THIS SCHEMA IS NOT COMPLEAT, it does not cover constraints or foreign keys
-- Its purpose is only to gather all attributes in one place for easier further development

CREATE TABLE AgeRestrictions (
	age_restriction_name CHAR,
	PRIMARY KEY(age_restriction_name)
);

CREATE TABLE Languages (
	id_language INTEGER,
	language_name CHAR,
	PRIMARY KEY(id_language)
);

CREATE TABLE CinemaUsers (
	id_user INTEGER,
	name CHAR,
	surname CHAR,
	email CHAR,
	password CHAR,
	birth DATE,
	PRIMARY KEY(id_user)
);

CREATE TABLE Rooms (
	id_room INTEGER,
	room_sign CHAR,
	floor_number NUMBER,
	imax_capable BOOLEAN,
	wheelchair_availability BOOLEAN,
	sponsor CHAR,
	capable_3D BOOLEAN,
	PRIMARY KEY(id_room)
);

CREATE TABLE Seats (
	id_seat INTEGER,
	seat_row INTEGER,
	seat_number INTEGER,
	is_vip_seat BOOLEAN,
	fk_room INTEGER,
	fk_connected_seat INTEGER,
	PRIMARY KEY(id_seat)
);

CREATE TABLE Movies (
	id_movie INTEGER,
	name CHAR,
	premiere DATE,
	duration INTEGER,
	is_imax BOOLEAN,
	fk_language INTEGER,
	fk_age_restriction CHAR,
	PRIMARY KEY(id_movie)
);

CREATE TABLE MovieVersions (
	id_movie_version INTEGER,
	dimension CHAR,
	fk_dubbing_language INTEGER,
	fk_subtitles_language INTEGER,
	fk_voice_over_language INTEGER,
	fk_movie INTEGER,
	PRIMARY KEY(id_movie_version)
);

CREATE TABLE Shows (
	id_show INTEGER,
	start_hour INTEGER,
	start_minute INTEGER,
	show_date DATE,
	fk_room INTEGER,
	fk_movie_version INTEGER,
	PRIMARY KEY(id_show)
);

CREATE TABLE Tickets (
	id_ticket INTEGER,
	discount FLOAT,
	base_price FLOAT,
	purchase TIMESTAMP,
	fk_seat INTEGER,
	fk_show INTEGER,
	fk_user INTEGER,
	PRIMARY KEY(id_ticket)
);

