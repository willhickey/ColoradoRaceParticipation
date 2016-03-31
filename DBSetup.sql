--This project uses SQLite. This SQL builds the initial DB:
>sqlite3 BRACData.db

CREATE TABLE "Event" (
	`ID`	int,
	`EventName`	text,
	`EventDate`	text,
	`EventType`	text,
	`EventYear`	INTEGER,
	PRIMARY KEY(ID)
)

CREATE TABLE EventCategory (EventID int, Category text, Starters int, Finishers int)