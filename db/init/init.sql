-- Defines our schema and initial relations

-- Tables
--CREATE TABLE trains (id int, name char(40));
                                       
CREATE TABLE Passenger(id int PRIMARY KEY, first_name char(50), last_name char(50), phone_number char(20), email char(50), address char(150), FOREIGN KEY address REFERENCES address (Address)) 

CREATE TABLE Address(address char(150) PRIMARY KEY, city char(50))
                                                              
CREATE TABLE Ticket(seat_number int, passenger_id int, class_type char(20) NOT NULL, trip_id int NOT NULL, PRIMARY KEY (seat_number, trip_id), FOREIGN KEY passenger_id REFERENCES Passenger (id), FOREIGN KEY class_type REFERENCES Class (type), FOREIGN KEY trip_id REFERENCES Trip (id))

CREATE TABLE Class (type char(20) PRIMARY KEY, refundable boolean, priority_boarding boolean, free_food boolean) 

CREATE TABLE Train (id int PRIMARY KEY, capacity int)

CREATE TABLE Train_Has_Class (train_id int, class_type char(20), PRIMARY KEY (train_id, class_type), FOREIGN KEY train_id REFERENCES Train (id), FOREIGN KEY class_type REFERENCES Class (type))

CREATE TABLE Worker (id int PRIMARY KEY, first_name char(50), last_name char(50), phone_number char(20), availability char(10)) 
                                                                                                                           
CREATE TABLE Maintenance_Worker (worker_id int PRIMARY KEY, FOREIGN KEY worker_id REFERENCES Worker(id)) 
                                                                                                   
CREATE TABLE Works_On (maintenance_worker_id int, segment_id int, PRIMARY KEY (maintenance_worker_id, segment_id), FOREIGN KEY maintenance_worker_id REFERENCES Maintenance_Worker(id), FOREIGN KEY segment_id REFERENCES Segment(id) ON DELETE CASCADE) 

CREATE TABLE Train_Worker (worker_id int PRIMARY KEY, FOREIGN KEY worker_id REFERENCES Worker(id)) 
                                                                                             
CREATE TABLE Works_Shift (train_worker_id int, trip_id int, segment_id int PRIMARY KEY (train_worker, trip_id, segment_id), FOREIGN KEY train_worker_id REFERENCES Train_Worker(id), FOREIGN KEY trip_id REFERENCES Trip(id), FOREIGN KEY segment_id REFERENCES Segment(id)) 

CREATE TABLE Station_Worker (worker_id int PRIMARY KEY, works_at_station_name char(20), FOREIGN KEY worker_id REFERENCES Worker(id), FOREIGN KEY works_at_station_name REFERENCES Station(name)) 

CREATE TABLE Station (name char(50) PRIMARY KEY, location char(50), capacity int) 

CREATE TABLE Segment (id int PRIMARY KEY, track_length char(50),condition char(50), start_station_name char(20) NOT NULL, end_station_name char(20) NOT NULL, FOREIGN KEY (start_station_name) REFERENCES Station (name), FOREIGN KEY (end_station_name) REFERENCES Station (name)) 

CREATE TABLE Trip (id int PRIMARY KEY, departure_time char(5), arrival_time char(5)) 
                                                                                
CREATE TABLE Trip_Leg (trip_id int, segment_id int, train_id int NOT NULL, PRIMARY KEY (trip_id, segment_id), FOREIGN KEY (trip_id) REFERENCES Trip (id), FOREIGN KEY (segment_id) REFERENCES Segment (id))

CREATE TABLE Works_Shift(train_worker_id int, trip_id int, segment_id int, hours int,
time char(5), PRIMARY KEY (train_worker_id, trip_id, segment_id), FOREIGN KEY (train_worker_id) REFERENCES Train_Worker (worker_id), FOREIGN KEY (trip_id) REFERENCES Trip (id), FOREIGN KEY (segment_id) REFERENCES Segment (id))


-- Tuples
--INSERT INTO trains VALUES (1, 'Thomas');
--INSERT INTO trains VALUES (2, 'Elliot');

INSERT INTO Passenger VALUES (1,'John','Smity','(124)-333-3214','uad@gmail.com','321 41 St');
INSERT INTO Passenger VALUES (2,'Carley','Craft','(125)-365-3214','51d@gmail.com','451 49 Ave');
INSERT INTO Passenger VALUES (3,'Darryl','Lim','(129)-313-3214','gfsd@gmail.com','3 Red St');
INSERT INTO Passenger VALUES (4,'Lester','Morley','(132)-532-3214','gjss@gmail.com','3 3rd Ave');
INSERT INTO Passenger VALUES (5,'Huzaifa','Connelly','(112)-123-3214','djj@gmail.com','994 3rd St');

INSERT INTO Address VALUES ('321 41St','Vancouver');
INSERT INTO Address VALUES ('451 49Ave','Delta');
INSERT INTO Address VALUES ('3 Red St','Calgary');
INSERT INTO Address VALUES ('3 3rd Ave','Toronto');
INSERT INTO Address VALUES ('994 3rd st','Halifax');

INSERT INTO Ticket VALUES (1,3,'First',1);
INSERT INTO Ticket VALUES (2,2,'First',1);
INSERT INTO Ticket VALUES (3,1,'Business',1);
INSERT INTO Ticket VALUES (34,5,'Economy',2);
INSERT INTO Ticket VALUES (1,4,'First',4);

INSERT INTO Class VALUES ('First',true,true,true);
INSERT INTO Class VALUES ('Business',true,true,true);
INSERT INTO Class VALUES ('Standard',true,true,false);
INSERT INTO Class VALUES ('Affordable',true,false,false);
INSERT INTO Class VALUES ('Basic',false,false,false);

INSERT INTO Train VALUES (1,100);
INSERT INTO Train VALUES (2,200);
INSERT INTO Train VALUES (3,300);
INSERT INTO Train VALUES (4,300);
INSERT INTO Train VALUES (5,250);

INSERT INTO Train_Has_Class VALUES (1,'Standard');
INSERT INTO Train_Has_Class VALUES (1,'Basic');
INSERT INTO Train_Has_Class VALUES (3,'First');
INSERT INTO Train_Has_Class VALUES (3,'Business');
INSERT INTO Train_Has_Class VALUES (3,'Standard');

INSERT INTO Worker VALUES (1,'Sean','Dale','(124)-985-4832','Mechanical Engineer','M T W Th F');
INSERT INTO Worker VALUES (2,'Kaiya','Cantrell','(653)-452-4382','Office Administrator','M W F');
INSERT INTO Worker VALUES (3,'Marc','Padilla','(623)-874-1983','CEO','Sa Su M T W F');
INSERT INTO Worker VALUES (4,'Wilf','Fischer','(875)-983-4572','Conductor','Sa M F');
INSERT INTO Worker VALUES (5,'Amy-Louise','Boyd','(234)-239-1432','Ticket Salesperson','Sa W Th F');
INSERT INTO Worker VALUES (6,'Trevor','Siemian','(232)-242-2322','Mechanical Engineer','M T W Th F');
INSERT INTO Worker VALUES (7,'Sam','Bradford','(534)-234-9595','Maintenance Technician','M T W Th F');
INSERT INTO Worker VALUES (8,'Kelly','Gregg','(484)-344-2200','Maintenance Technician','M T W Th F');
INSERT INTO Worker VALUES (9,'Andrea','Bocelli','(623)-239-0003','Supervisor, Maintenance','M T W Th F');
INSERT INTO Worker VALUES (10,'Bob','Wagner','(334)-593-9494','Conductor','M T W Th F');
INSERT INTO Worker VALUES (11,'Marc','Jacobs','(899)-393-2289','Ticket Salesperson','F Sa Su M');
INSERT INTO Worker VALUES (12,'Nick','Cannon','(893)-394-3940','Service Attendant','F Sa Su M');
INSERT INTO Worker VALUES (13,'Jon','Gruden','(604)-293-2920','Service Attendant','F Sa Su M');
INSERT INTO Worker VALUES (14,'Alice','Wonderland','(778)-393-9943','Station Manager','M T W Th F');
INSERT INTO Worker VALUES (15,'Jack','Wilshere','(204)-294-9955','CFO','M T W Th F');

INSERT INTO Maintenance_Worker VALUES (1);
INSERT INTO Maintenance_Worker VALUES (6);
INSERT INTO Maintenance_Worker VALUES (7);
INSERT INTO Maintenance_Worker VALUES (8);
INSERT INTO Maintenance_Worker VALUES (9);

INSERT INTO Works_On VALUES (1,1);
INSERT INTO Works_On VALUES (6,2);
INSERT INTO Works_On VALUES (7,3);
INSERT INTO Works_On VALUES (8,4);
INSERT INTO Works_On VALUES (9,5);

INSERT INTO Train_Worker VALUES (4);
INSERT INTO Train_Worker VALUES (10);
INSERT INTO Train_Worker VALUES (11);
INSERT INTO Train_Worker VALUES (12);
INSERT INTO Train_Worker VALUES (13);

INSERT INTO Works_Shift VALUES (4,1,1,8,'8:00');
INSERT INTO Works_Shift VALUES (10,2,2,6,'8:00');
INSERT INTO Works_Shift VALUES (11,3,3,7,'10:00');
INSERT INTO Works_Shift VALUES (12,4,4,8,'13:00');
INSERT INTO Works_Shift VALUES (13,5,5,8,'14:00');

INSERT INTO Station_Worker VALUES (2,'Central');
INSERT INTO Station_Worker VALUES (3,'Central');
INSERT INTO Station_Worker VALUES (5,'South');
INSERT INTO Station_Worker VALUES (14,'East');
INSERT INTO Station_Worker VALUES (15,'West');

INSERT INTO Station VALUES ('Central','Central City',100);
INSERT INTO Station VALUES ('East','Port City',100);
INSERT INTO Station VALUES ('West','Foothills',10);
INSERT INTO Station VALUES ('North','Mount Pleasant',20);
INSERT INTO Station VALUES ('South','Arbor City',30);

INSERT INTO Segment VALUES (1,100,NULL,'East','West');
INSERT INTO Segment VALUES (2,200,NULL,'East','Central');
INSERT INTO Segment VALUES (3,150,'Broken','Central','West');
INSERT INTO Segment VALUES (4,80,NULL,'West','North');
INSERT INTO Segment VALUES (5,300,NULL,'South','North');

INSERT INTO Trip VALUES (1,'12:00','18:00');
INSERT INTO Trip VALUES (2,'10:00','20:00');
INSERT INTO Trip VALUES (3,'6:00','10:00');
INSERT INTO Trip VALUES (4,'5:00','9:00');
INSERT INTO Trip VALUES (5,'8:00','12:00');

INSERT INTO Trip_Leg VALUES (1,2,1);
INSERT INTO Trip_Leg VALUES (2,3,2);
INSERT INTO Trip_Leg VALUES (3,5,3);
INSERT INTO Trip_Leg VALUES (4,4,4);
INSERT INTO Trip_Leg VALUES (5,1,5);
