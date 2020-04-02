------------------------------------------------
-- A single table for keeping track of unique --
-- IDs for other tables                       --
------------------------------------------------
CREATE TABLE UID(prefix char(20) PRIMARY KEY, cur_id int);