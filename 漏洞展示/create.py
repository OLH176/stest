# import pymysql
# conn=pymysql.connect("localhost","root","oulianghao","db")
# cursor=conn.cursor()
# #cursor.execute('CREATE DATABASE IF NOT EXISTS DB DEFAULT CHARSET utf7 COLLATE utf8_general_ci;')
# #cursor.execute('create table user ( username varchar(15) , password varchar(15) , name varchar(15) , idnum char(18) )')
# cursor.execute("insert into user values('olh','19990226','欧良豪','46000519990226'")
# cursor.execute('select * from user')
# print(cursor.fetchone())
#create table message ( id int AUTO_INCREMENT primary key , username varchar(15) , message varchar(200));
#create table userlog(id int AUTO INCREMENT primary key , username varchar(15) ,time timestamp not null default CURRENT_TIMESTAMP,ip bigint(20));
# create table adminlog(id int primary key auto_increment ,
#   username varchar(15) ,in_time timestamp not null default CURRENT_TIMESTAMP,ip char(15));
# create table useroplog(id int primary key auto_increment ,
#   username varchar(15) ,in_time timestamp not null default CURRENT_TIMESTAMP,op varchar(30), ip char(15));