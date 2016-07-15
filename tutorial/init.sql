create database if not exists `12306-train`;

grant usage on *.* to '12306'@'localhost';
drop user '12306'@'localhost';

create user '12306'@'localhost' identified by '12306'; 
grant all privileges on `12306-train`.* to '12306'@'localhost';
