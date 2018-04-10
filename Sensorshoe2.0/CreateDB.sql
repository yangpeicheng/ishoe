create database sensorshoe;

use sensorshoe;
create table users(
    id int,
    user_name varchar(32),
    sex varchar(4),
    birthday date
);

create table sensors(
	id int,
	mac_addr varchar(32) not null,
    host_id int,
    status int
);

create table sensorsdata(
	time_stamp varchar(32) not null,
	mac_addr varchar(32) not null,
    lux float,
    accx float,
    accy float,
    accz float,
    gyrox float,
    gyroy float,
    gyroz float,
    magx float,
    magy float,
    magz float
);