drop database if exists 4question;
create database 4question;

use 4question;



create table information (
id int auto_increment primary key,
client_name varchar(255),
telephone int(10),
email varchar(255),
orders varchar(255),
order_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
order_status ENUM('Выполнен','В работе','Новый')

);




INSERT INTO information (client_name, telephone, email, order_data, order_status)
VALUES 
('Иван Иванов', 1234567890, 'ivanov@example.com', '2023-10-01 10:30:00', 'Выполнен'),
('Мария Петрова', 2345678901, 'petrova@example.com', '2023-10-02 14:45:00', 'Новый'),
('Сергей Сидоров', 3456789012, 'sidorov@example.com', '2023-10-03 09:15:00', 'В работе'),
('Анна Смирнова', 4567890123, 'smirnova@example.com', '2023-10-04 16:50:00', 'Выполнен'),
('Николай Федоров', 5678901234, 'fedorov@example.com', '2023-10-05 11:20:00', 'Новый');


select * from information;
