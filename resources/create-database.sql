create database busboy
        encoding = 'utf8';

\connect busboy

create table passage_responses (
        route_id varchar(30),
        direction smallint,
        vehicle_id varchar(30),
        last_modified timestamp,
        trip_id varchar(30),
        congestion_level smallint,
        accuracy_level smallint,
        status smallint,
        is_accessible boolean,
        latitude integer,
        longitude integer,
        bearing integer,
        pattern_id varchar(30),
        has_bike_rack boolean,
        category smallint,
        primary key (trip_id, last_modified)
);

create table routes (
        id varchar(30) primary key,
        name varchar(20),
        direction smallint,
        number integer,
        category smallint
);

create table stops (
        id varchar(30) primary key,
        name varchar(50),
        number integer,
        latitude double precision,
        longitude double precision
);

create table timetables (
        id int generated always as identity primary key,
        caption text
);

create table route_timetables (
        route varchar(30) references routes(id),
        timetable int references timetables(id),
        primary key (route, timetable)
);

create table timetable_variants (
        id int generated always as identity primary key,
        route_name varchar(10),
        timetable_id int references timetables(id)
);

create table variant_stops (
        position int,
        variant int references timetable_variants(id),
        stop varchar(30) references stops(id),
        primary key (variant, position)
);
