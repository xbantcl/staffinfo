drop table if exists user_info;
create table user_info(
    id integer primary key autoincrement,
    username varchar(20) not null,
    pingyinname varchar(20) not null,
    email varchar(20) not null,
    office_num varchar(15) not null,
    mobile varchar(15) not null,
    department varchar(15) not null
);
