import sqlite3
import csv
import os

conn = sqlite3.connect('C:/Users/user/yes24.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS book_info;")
cur.execute("""CREATE TABLE book_info(
    bookname varchar(128),
    salesindex float,
    rating float,
    price int,
    reviewcount int,
    totalpage int,
    weight int,
    size varchar(32),
    category varchar(32),
    releasedate DATETIME
);"""
            )

users = []

with open('C:/Users/user/yes24_save.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i in reader:
        users.append(i)

for user in users[1:]:
    cur.execute("""INSERT INTO book_info(
                bookname, salesindex, rating, price, reviewcount, totalpage, weight, size, category, releasedate) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                ,(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9]))

conn.commit()
