#!/usr/bin/python3
import json
from typing import List
import requests
from bs4 import BeautifulSoup
import sqlite3

def InsertToDatabase(gpuList):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO Gpus(Title, Price) VALUES (?, ?)"""

        cursor.executemany(sqlite_insert_query, gpuList)
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records inserted successfully into Gpus table")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

try:
    html_text = requests.get('https://www.skroutz.gr/c/55/kartes-grafikwn-vga.html?o=gpu').text
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)
else:
    list = []
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    sqlite_create_table_query = '''CREATE TABLE Gpus (
                                Title TEXT NOT NULL, Price TEXT NOT NULL)'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    soup = BeautifulSoup(html_text, 'lxml')
    gpus = soup.findAll('li', class_ = 'cf card')
    for gpu in gpus:
        gpu_content = gpu.find('div', class_ = 'card-content')
        gpu_title = gpu_content.find('a', class_ = 'js-sku-link').get('title')
        gpu_price = gpu_content.find('a',class_ = 'js-sku-link sku-link').text.replace('€','').replace('από','')
        GPU=(gpu_title,gpu_price)
        list.append(GPU)
    InsertToDatabase(list)

    sqlite_select_query = """SELECT * from Gpus"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row:")
    for row in records:
        print("Title: ", row[0])
        print("Price: ", row[1])
    cursor.close()

