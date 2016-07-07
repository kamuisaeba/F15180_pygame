create database if not exists snake;
use snake;
create table if not exists config (music bit,sound bit);
create table if not exists ranking (user varchar(255),score int);
insert into config (music,sound) values (1,1);
