sqlite3 class.db
create table class(id int primary key, lname text,fname);
insert into class values (1, "Wayne", "Bruce");
insert into class values (2, "Jennifer", "Walters");

create table superhero(id int primary key, alias text);
insert into superhero values (1, "Batman");
insert into superhero values (2, "She-Hulk");

create table superhero_name as select * from  class left join superhero using(id);
select * from superhero_name;