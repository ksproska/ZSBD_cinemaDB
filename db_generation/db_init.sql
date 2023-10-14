CREATE TABLE AgeRestriction(
	age_restriction_name CHAR
	PRIMARY KEY()
);
CREATE TABLE Language(
	id_language INTEGER
	language_name CHAR
	PRIMARY KEY()
);
CREATE TABLE User(
	id_user INTEGER
	name CHAR
	surname CHAR
	email CHAR
	password CHAR
	birth DATE
	PRIMARY KEY()
);
CREATE TABLE Room(
	id_room INTEGER
	room_sign CHAR
	floor_number NUMBER
	imax_capable BOOLEAN
	wheelchair_availability BOOLEAN
	sponsor CHAR
	capable_3D BOOLEAN
	PRIMARY KEY()
);
CREATE TABLE Seat(
	id_seat INTEGER
	row INTEGER
	number INTEGER
	is_vip_seat BOOLEAN
	fk_room INTEGER
	PRIMARY KEY()
);
