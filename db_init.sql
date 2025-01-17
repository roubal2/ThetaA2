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
created_at datetime default current_timestamp,
foreign key (category_id) references categories(category_id)
);

create table orders(
order_id int auto_increment primary key,
user_id int not null,
order_total float default 0.0,
order_status enum('Confirmed', 'In-Transit', 'Delivered', 'Refunded') not null default 'Confirmed',
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
select u.user_id, u.username, o.order_id, o.order_date, o.order_total, o.order_status
from users u
join orders o on u.user_id = o.user_id;

create view view_category_products as
select c.category_name, p.product_id, p.product_name, p.price
from categories c 
join products p on c.category_id = p.category_id;


delimiter //
create trigger OrderTotal
after insert on orderItems
for each row
begin 
	update orders
	set order_total = (
		select sum(p.price * oi.quantity)
        from orderItems oi
        join products p on oi.product_id = p.product_id
        where oi.order_id = new.order_id
    )
    where order_id = new.order_id;
    
end //
delimiter ;

set foreign_key_checks = 1;
truncate table users;
truncate table products;
truncate table orders;
truncate table orderItems;
truncate table categories;
select * from users;
select * from orders;
select * from products;
select * from orderItems;
select * from categories;