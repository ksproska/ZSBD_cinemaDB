create table AgeRestriction
(
    age_restriction_name varchar2(50) primary key
);

create table CinemaUser
(
    id_user  number primary key,
    name     varchar2(10) not null,
    surname  varchar2(10) not null,
    email    varchar2(50) not null,
    password varchar2(20) not null,
    birth    date not null
);

create table Room
(
    id_room                 number primary key,
    room_sign               varchar2(20) not null,
    floor_number            number not null,
    imax_capable            varchar2(1) check (imax_capable in ('Y', 'N')) not null,
    wheelchair_availability varchar2(1) check (wheelchair_availability in ('Y', 'N')) not null,
    sponsor                 varchar2(50),
    capable_3D           varchar2(1) check (capable_3D in ('Y', 'N')) not null
);

create table Language
(
    id_language varchar2(10) primary key,
    language_name varchar2(50) not null
);

create table Movie
(
    id_movie           number primary key,
    name               varchar2(100) not null,
    premiere      date,
    duration           number not null,
    is_imax            varchar2(1) check (is_imax in ('Y', 'N')) not null,
    fk_age_restriction varchar2(50),
    fk_language        varchar2(10),

    foreign key (fk_age_restriction)
        references AgeRestriction (age_restriction_name),
    foreign key (fk_language)
        references Language (id_language)
);

create table MovieVersion
(
    id_movie_version       number primary key,
    dimension              varchar2(10) not null,
    fk_subtitles_language  varchar2(10),
    fk_dubbing_language    varchar2(10),
    fk_voice_over_language varchar2(10),
    fk_movie               number,

    foreign key (fk_subtitles_language)
        references Language (id_language),
    foreign key (fk_dubbing_language)
        references Language (id_language),
    foreign key (fk_voice_over_language)
        references Language (id_language),
    foreign key (fk_movie)
        references Movie (id_movie)
);

create table Show
(
    id_show          number primary key,
    show_date        date not null,
    start_hour       number not null,
    start_minute     number not null,
    fk_room          number,
    fk_movie_version number,

    foreign key (fk_room)
        references Room (id_room),
    foreign key (fk_movie_version)
        references MovieVersion (id_movie_version)
);

create table Seat
(
    id_seat           number primary key,
    seat_row          number not null,
    seat_number       number not null,
    is_vip_seat       varchar2(1) check ( is_VIP_seat in ('Y', 'N') ) not null,
    fk_room           number,
    fk_connected_seat number,

    foreign key (fk_room)
        references Room (id_room),
    foreign key (fk_connected_seat)
        references Seat (id_seat)
);

create table Ticket
(
    id_ticket number primary key,
    discount  float,
    base_price     float not null,
    purchase  timestamp,
    fk_seat   number,
    fk_show   number,
    fk_user   number,

    foreign key (fk_seat)
        references Seat (id_seat),
    foreign key (fk_show)
        references Show (id_show),
    foreign key (fk_user)
        references CinemaUser (id_user)
);