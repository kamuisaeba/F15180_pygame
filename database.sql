create database if not exists snake;
use snake;
create table if not exists ranking (user varchar(255),score int,level int);
create user snake identified by 'snake'
grant all privilleges from snake.* to 'snake'@localhost
