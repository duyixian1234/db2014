CREATE TABLE `book` (
  `bno` varchar(20) NOT NULL DEFAULT '',
  `category` char(50) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `press` varchar(50) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `price` decimal(7,2) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  PRIMARY KEY (`bno`)
) E

CREATE TABLE `card` (
  `cno` char(7) NOT NULL,
  `name` varchar(10) DEFAULT NULL,
  `department` varchar(40) DEFAULT NULL,
  `type` enum('T','G','U','O') DEFAULT NULL,
  PRIMARY KEY (`cno`)
)

CREATE TABLE `manager` (
  `id` char(10) NOT NULL,
  `passwd` char(16) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `tel` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
)

 CREATE TABLE `borrow` (
  `cno` char(7) NOT NULL,
  `bno` char(8) DEFAULT NULL,
  `borrow_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `id` char(10) DEFAULT NULL,
  KEY `cno` (`cno`),
  KEY `bno` (`bno`),
  KEY `id` (`id`),
  CONSTRAINT `borrow_ibfk_1` FOREIGN KEY (`cno`) REFERENCES `card` (`cno`) ON UPDATE CASCADE,
  CONSTRAINT `borrow_ibfk_2` FOREIGN KEY (`bno`) REFERENCES `book` (`bno`) ON UPDATE CASCADE,
  CONSTRAINT `borrow_ibfk_3` FOREIGN KEY (`id`) REFERENCES `manager` (`id`) ON UPDATE CASCADE
)

create trigger borrow_limit before insert on borrow
for each row
begin
        declare num int;
select stock into num from book where bno=new.bno;
if num=0 then
set new.cno=NULL;
end if;
end |
