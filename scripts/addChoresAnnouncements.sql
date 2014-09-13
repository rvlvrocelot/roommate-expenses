drop table if exists weeklyChores;
create table weeklyChores (
  id integer primary key autoincrement,
  person text not null,
  choreid integer not null,
  completed int not null
);

Insert into weeklyChores (person, chore, completed)
values("Ryder","Kitchen", 0);
Insert into weeklyChores (person, chore, completed)
values("Andrew","Bathroom", 0);
Insert into weeklyChores (person, chore, completed)
values("Anita","Floors/Trash", 0);

drop table if exists announcements;
create table announcements (
  id integer primary key autoincrement,
  user text not null, 
  Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  announcement text not null,
  details text not null
);

