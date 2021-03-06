drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  expense text not null,
  amount int not null,
  note text not null,
  name text not null
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  pass text not null
);

Insert into users (username, pass)
values ("Anita","de9d3c9be378d81b0244502a0f075b50");
Insert into users (username, pass)
values ("Andrew","566389c28abc48e488ac56d57fc338fa");
Insert into users (username, pass)
values ("Ryder","3717a626cab4016cb5066212cd97b189");

drop table if exists payments;
create table payments (
  id integer primary key autoincrement,
  payer text not null,
  payee text not null,
  amount int default 0  
);

Insert into payments (payer, payee, amount)
values ("Andrew","Anita",0);
Insert into payments (payer, payee, amount)
values ("Andrew","Ryder",0);
Insert into payments (payer, payee, amount)
values ("Anita","Ryder",0);

drop table if exists paymentHistory;
create table paymentHistory (
  id integer primary key autoincrement,
  payer text not null,
  payee text not null,
  amount int default 0,
  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  
);

drop table if exists weeklyChores;
create table weeklyChores (
  id integer primary key autoincrement,
  person text not null,
  choreid integer not null,
  completed int not null
);

drop table if exists choreList;
create table choreList (
  id integer primary key autoincrement,
  choreid integer not null,
  choreSub text not null,
  subComplete text not null
);

drop table if exists choreDesc;
create table choreDesc (
  id integer primary key autoincrement,
  choreid integer not null,
  desc text not null
);

Insert into weeklyChores (person, choreid, completed)
values("Ryder",0, 0);
Insert into weeklyChores (person, choreid, completed)
values("Andrew",1, 0);
Insert into weeklyChores (person, choreid, completed)
values("Anita",2, 0);

Insert into choreDesc(choreid,desc)
values(0,"Kitchen Duty");
Insert into choreDesc(choreid,desc)
values(1,"Bathroom Duty");
Insert into choreDesc(choreid,desc)
values(2,"Livingroom Duty");

Insert into choreList (choreid, choreSub, subComplete)
values(0, "Clean kitchen counter",0);
Insert into choreList (choreid, choreSub, subComplete)
values(0, "Clean stove top",0);
Insert into choreList (choreid, choreSub, subComplete)
values(0, "Clear expired food from fridge",0);
Insert into choreList (choreid, choreSub, subComplete)
values(0, "Clean Microwave",0);

Insert into choreList (choreid, choreSub, subComplete)
values(1, "Clean bathroom counter top",0);
Insert into choreList (choreid, choreSub, subComplete)
values(1, "Clean toilet",0);
Insert into choreList (choreid, choreSub, subComplete)
values(1, "Clean tub",0);
Insert into choreList (choreid, choreSub, subComplete)
values(1, "Ensure bathroom floor is clean",0);

Insert into choreList (choreid, choreSub, subComplete)
values(2, "Sweep living room floors",0);
Insert into choreList (choreid, choreSub, subComplete)
values(2, "Dust coffee table",0);
Insert into choreList (choreid, choreSub, subComplete)
values(2, "Wipe down kitchen table",0);
Insert into choreList (choreid, choreSub, subComplete)
values(2, "Take out trash (Monday or Tuesday)",0);
Insert into choreList (choreid, choreSub, subComplete)
values(2, "Take out trash (Wednesday or Thursday)",0);
Insert into choreList (choreid, choreSub, subComplete)
values(2, "Take out trash (Friday or Saturday)",0);


drop table if exists announcements;
create table announcements (
  id integer primary key autoincrement,
  user text not null, 
  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  announcement text not null,
  details text not null
);



