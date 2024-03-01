# MariDB 데이터베이스 리스트 조회
show databases;

# myapp DB 생성 및 사용
create database myapp;
use myapp;

# tbl_users 테이블 생성
create table tbl_users (
	id int(10) not null auto_increment primary key, 
    name varchar(20),
    email varchar(100),
    password varchar(100)
);

# 행 추가
insert into tbl_users (name, email, password) values ('baek', 'baek@naver.com', '1111');

# 테이블 전체 데이터 조회
select * from tbl_users;

# 테이블 조건 (where) 조회
select * from tbl_users where email = 'baek@naver.com' and password = '1111';
