
use `12306-train`;

drop table if exists `agencys`;

create table `agencys` (
    `province` varchar(10) not null,
    `city` varchar(15) not null,
    `county` varchar(15) not null,
    `address` varchar(50) primary key,
    `name` varchar(50) not null,
    `windows` int,
    `start` time,
    `end` time
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

