CREATE TABLE Orders(
	OrderId int NOT NULL IDENTITY PRIMARY KEY,
	OrderDateTime datetime default CURRENT_TIMESTAMP,
	Amount float,
	Country nvarchar(50)
);

INSERT INTO Orders(Amount,Country)
VALUES(100,'United States of America')

INSERT INTO Orders(Amount,Country)
VALUES (250,'Canada')

INSERT INTO Orders(Amount,Country)
VALUES (75,'United States of America')

INSERT INTO Orders(Amount,Country)
VALUES (90,'United States of America')

INSERT INTO Orders(Amount,Country)
VALUES (40,'Canada')

INSERT INTO Orders(Amount,Country)
VALUES (100,'Mexico')

INSERT INTO Orders(Amount,Country)
VALUES (75, 'Brazil')

-- DROP TABLE Orders;


CREATE TABLE books(
	id int IDENTITY PRIMARY KEY,
	upc nvarchar(100),
	product_type nvarchar(100),
	title nvarchar(100),
	page_url nvarchar(200),
	image_url nvarchar(200),
	rating nvarchar(100),
	availability nvarchar(100),
	number_of_reviews nvarchar(100),
	price float,
	price_without_tax float,
	price_with_tax float,
	tax float
);