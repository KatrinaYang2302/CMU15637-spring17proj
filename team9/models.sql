create table User(
	username char(255),
	first_name char(255),
	last_name char(255),
	e_mail char(255),
	phone_number int(11),
	password char(16),
	primary key (username)
);

create table fav_place(
	username char(255),
	place_name char(255),
	place_lat double,
	place_long double,
	primary key (username, place_name),
	foreign key (username) references User (username) on delete cascade
);

create table rt(
	rt_no char(4),
	rt_name char(32),
	primary key (rt_no)
);

create table fav_rt(
	username char(255),
	rt_no char(4),
	primary key (username, rt_no),
	foreign key (username) references User (username) on delete cascade,
	foreign key (rt_no) references rt (rt_no) on delete cascade
);

create table stops(
	stop_id int(6),
	stop_name char(255),
	stop_long double,
	stop_lat double,
	primary key (stop_id)
);

create table rt_stop(
	rt_no char(4),
	stop_id int(6),
	dir char(16),
	dist double,
	primary key (rt_no, stop_id),
	foreign key (rt_no) references rt (rt_no) on delete cascade,
	foreign key (stop_id) references stops (stop_id) on delete cascade
);