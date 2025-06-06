drop view if exists customer_capital_gain_view;
drop table if exists company_balance;
drop table if exists customer_balance;
drop table if exists sell_list;
drop table if exists buy_list;
drop table if exists order_list;
drop table if exists financial_info;
drop table if exists company;
drop table if exists admin;
drop table if exists account;

create table account (
	id varchar(10) unique,
	password varchar(12),
	a_number numeric(8, 0) check (a_number > 0) unique,
	type varchar(8),
	name varchar(20),
	phone char(13),
	cash bigInt check (cash >= 0),
	capital_gain bigInt,
	
	primary key (a_number)
);

create table admin (
	id varchar(10),
	password varchar(12),
	type char(5),

	primary key (id)
);

create table company (
	name varchar(20),
	price bigInt check (price >= 1),
	stock_num bigInt check (stock_num >= 1),
	total_price bigInt check (total_price >= 1),
	sector varchar(25),

	primary key (name)
);

create table financial_info (
	name varchar(20),
	year numeric(4, 0) check (year >= 1900),
	sales bigInt check (sales >= 0),
	business_profits bigInt,
	pure_profits bigInt,
	
	primary key (name, year),
	foreign key (name) references company
		on delete cascade

);

create table order_list (
	a_number numeric(8, 0),
	type varchar(4),
	name varchar(20),
	price bigInt check (price >= 1),
	count bigInt check (count >= 1),
	order_number bigserial check (order_number >= 1) unique,	

	primary key (a_number, order_number),
	foreign key (a_number) references account
		on delete cascade
);

create table buy_list (
	buy_list_number bigserial check (buy_list_number >= 1) unique,
	a_number numeric(8, 0),
	name varchar(20),
	price bigInt check (price >= 1),
	b_date date,
	b_time time,
	b_count bigInt check (b_count >= 1),
	s_count bigInt check (b_count >= s_count and s_count >= 0),
	
	primary key (a_number, buy_list_number),
	foreign key (a_number) references account
		on delete cascade
);

create table sell_list (
	sell_list_number bigserial check (sell_list_number >= 1) unique,
	a_number numeric(8, 0),
	name varchar(20),
	b_price bigInt check (b_price >= 1),
	s_price bigInt check (s_price >= 1),
	s_date date,
	s_time time,
	s_count bigInt check (s_count >= 1),

	primary key (a_number, sell_list_number),
	foreign key (a_number) references account
		on delete cascade
);

create table customer_balance (
	a_number numeric(8, 0),
	stock_name varchar(20),
	stock_count bigInt check (stock_count >= 0),
	avg_buy_price float check (avg_buy_price >= 1),
	

	primary key (a_number, stock_name),
	foreign key (a_number) references account
		on delete cascade,
	foreign key (stock_name) references company(name)
		on delete cascade
);

create table company_balance (
	a_number numeric(8, 0),
	stock_name varchar(20),
	stock_count bigInt check (stock_count >= 0),
	avg_buy_price float check (avg_buy_price >= 1),

	primary key (a_number, stock_name),
	foreign key (a_number) references account
		on delete cascade,
	foreign key (stock_name) references company(name)
		on delete cascade
);


CREATE ROLE mts_customer;
CREATE ROLE mts_admin;
CREATE ROLE mts_company;

GRANT mts_customer TO mts_user;
GRANT mts_admin TO mts_user;
GRANT mts_company TO mts_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO mts_customer, mts_admin, mts_company;
REVOKE INSERT, DELETE ON TABLE company FROM mts_customer, mts_company;
GRANT ALL ON SCHEMA public TO mts_admin;
























