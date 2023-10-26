CREATE TABLE AgeRestrictions
(
    age_restriction_name VARCHAR2(50) PRIMARY KEY
);

CREATE TABLE CinemaUsers
(
    id_user  NUMBER PRIMARY KEY,
    name     VARCHAR2(50) NOT NULL,
    surname  VARCHAR2(50) NOT NULL,
    email    VARCHAR2(50) NOT NULL,
    password VARCHAR2(50) NOT NULL,
    birth    DATE         NOT NULL
);

CREATE TABLE Rooms
(
    id_room                 NUMBER PRIMARY KEY,
    room_sign               VARCHAR2(50)                                              NOT NULL,
    floor_number            NUMBER                                                    NOT NULL,
    imax_capable            VARCHAR2(1) CHECK (imax_capable IN ('Y', 'N'))            NOT NULL,
    wheelchair_availability VARCHAR2(1) CHECK (wheelchair_availability IN ('Y', 'N')) NOT NULL,
    sponsor                 VARCHAR2(50),
    capable_3D              VARCHAR2(1) CHECK (capable_3D IN ('Y', 'N'))              NOT NULL
);

CREATE TABLE Languages
(
    id_language   VARCHAR2(50) PRIMARY KEY,
    language_name VARCHAR2(50) NOT NULL
);

CREATE TABLE Movies
(
    id_movie           NUMBER PRIMARY KEY,
    name               VARCHAR2(100)                             NOT NULL,
    premiere           DATE,
    duration           NUMBER                                    NOT NULL,
    is_imax            VARCHAR2(1) CHECK (is_imax IN ('Y', 'N')) NOT NULL,
    fk_age_restriction VARCHAR2(50),
    fk_language        VARCHAR2(50),

    FOREIGN KEY (fk_age_restriction)
        REFERENCES AgeRestrictions (age_restriction_name),
    FOREIGN KEY (fk_language)
        REFERENCES Languages (id_language)
);

CREATE TABLE MovieVersions
(
    id_movie_version       NUMBER PRIMARY KEY,
    dimension              VARCHAR2(50) NOT NULL,
    fk_subtitles_language  VARCHAR2(50),
    fk_dubbing_language    VARCHAR2(50),
    fk_voice_over_language VARCHAR2(50),
    fk_movie               NUMBER,

    FOREIGN KEY (fk_subtitles_language)
        REFERENCES Languages (id_language),
    FOREIGN KEY (fk_dubbing_language)
        REFERENCES Languages (id_language),
    FOREIGN KEY (fk_voice_over_language)
        REFERENCES Languages (id_language),
    FOREIGN KEY (fk_movie)
        REFERENCES Movies (id_movie)
);

CREATE TABLE Shows
(
    id_show          NUMBER PRIMARY KEY,
    show_date        DATE   NOT NULL,
    start_hour       NUMBER NOT NULL,
    start_minute     NUMBER NOT NULL,
    fk_room          NUMBER,
    fk_movie_version NUMBER,

    FOREIGN KEY (fk_room)
        REFERENCES Rooms (id_room),
    FOREIGN KEY (fk_movie_version)
        REFERENCES MovieVersions (id_movie_version)
);

CREATE TABLE Seats
(
    id_seat           NUMBER PRIMARY KEY,
    seat_row          NUMBER                                          NOT NULL,
    seat_number       NUMBER                                          NOT NULL,
    is_vip_seat       VARCHAR2(1) CHECK ( is_VIP_seat IN ('Y', 'N') ) NOT NULL,
    fk_room           NUMBER,
    fk_connected_seat NUMBER,

    FOREIGN KEY (fk_room)
        REFERENCES Rooms (id_room),
    FOREIGN KEY (fk_connected_seat)
        REFERENCES Seats (id_seat)
);

CREATE TABLE Tickets
(
    id_ticket  NUMBER PRIMARY KEY,
    discount   FLOAT,
    base_price FLOAT NOT NULL,
    purchase   TIMESTAMP,
    fk_seat    NUMBER,
    fk_show    NUMBER,
    fk_user    NUMBER,

    FOREIGN KEY (fk_seat)
        REFERENCES Seats (id_seat),
    FOREIGN KEY (fk_show)
        REFERENCES Shows (id_show),
    FOREIGN KEY (fk_user)
        REFERENCES CinemaUsers (id_user)
);
