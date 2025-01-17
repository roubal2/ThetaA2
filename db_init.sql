create database if not exists ThetaDB;
use ThetaDB;

create table users(
user_id int auto_increment primary key,
username varchar(255) unique not null,
email varchar(255) not null unique,
balance float not null check (balance >= 0) default 0.0,
is_active boolean default 0,
created_at datetime default current_timestamp
);

create table categories(
category_id int auto_increment primary key,
category_name varchar(255) unique not null
);

create table products(
product_id int auto_increment primary key,
category_id int not null,
product_name varchar(255) not null,
price float not null check (price >= 0) default 0.0,
product_status enum('Confirmed', 'In-Transit', 'Delivered', 'Refunded') not null,
created_at datetime default current_timestamp,
foreign key (category_id) references categories(category_id)
);

create table orders(
order_id int auto_increment primary key,
user_id int not null,
order_total float default 0.0,
order_date datetime default current_timestamp,
foreign key (user_id) references users(user_id)
);

create table orderItems(
order_item_id int auto_increment primary key,
order_id int not null,
product_id int not null,
quantity int not null default 1,
foreign key (order_id) references orders(order_id),
foreign key (product_id) references products(product_id)
);

create view view_user_orders as
select u.user_id, u.username, o.order_id, o.order_date, o.order_total
from users u
join orders o on u.user_id = o.user_id;

create view view_category_products as
select c.category_name, p.product_id, p.product_name, p.price, p.product_status
from categories c 
join products p on c.category_id = p.category_id;
