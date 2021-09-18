#!/usr/bin/python3
import json
from typing import List
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime




#Inserting scraped data to database
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



def ScrapingGpus():
    #Performing get request to below link to get html code
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
        #Connecting to database
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Gpus (
                                    Title TEXT  PRIMARY KEY NOT NULL , Price TEXT NOT NULL)'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        #Parsing html code
        soup = BeautifulSoup(html_text, 'lxml')
        gpus = soup.findAll('li', class_ = 'cf card')
        #Find all gpus and scraping info
        for gpu in gpus:
            gpu_content = gpu.find('div', class_ = 'card-content')
            gpu_title = gpu_content.find('a', class_ = 'js-sku-link').get('title')
            gpu_price = (gpu_content.find('a',class_ = 'js-sku-link sku-link').text.replace('€','').replace('από','').replace(' ','').replace(',','.').split('.'))
            gpu_price = gpu_price[0]+'.'+gpu_price[1]
            gpu_price = float(gpu_price)
            GPU=(gpu_title,gpu_price)
            list.append(GPU)
        InsertToDatabase(list)

#Retrieving data from database and printing in console
def RetrieveFromDb():
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    sqlite_select_query = """SELECT * from Gpus"""
    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query = """SELECT Title from Gpus"""
    cursor.execute(sqlite_select_query)
    gpuTitles = cursor.fetchall()

    sqlite_select_query = """SELECT Price from Gpus"""
    cursor.execute(sqlite_select_query)
    gpuPrices = cursor.fetchall()

    print("Total rows are:  ", len(records))
    print("Printing each row:")
    for row in records:
        print("Title: ", row[0])
        print("Price: ", row[1])
    cursor.close()
    return records


def CreateAndInsertIntoGpuTables(records):
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    for object in records:
        gpuTitle = str(object[0])
        gpuTitle = gpuTitle.replace(" ","_").replace("(","_").replace(")","_").replace(",","_").replace("'","_").replace(".","_").replace("-","_").replace("/","_")
        gpuPrice = float(object[1])
        
        helper = (gpuPrice,datetime.datetime.today().strftime("%d/%m/%Y"))

        sqlite_create_gpu_table_query = '''CREATE TABLE IF NOT EXISTS ''' + gpuTitle +'''(Price REAL NOT NULL,joiningDate timestamp)'''
        sqlite_insert_gpu_query = """INSERT INTO """ + gpuTitle +"""(Price, joiningDate) VALUES (?, ?)"""

        
        cursor.execute(sqlite_create_gpu_table_query)

        cursor.execute("""SELECT Price FROM """ + gpuTitle )
        tempPrice = cursor.fetchone()

        if(float(tempPrice[0]) ==  gpuPrice):
            cursor.execute('SELECT joiningDate FROM '+gpuTitle)
            tempDate=cursor.fetchone()
            created_date = datetime.datetime.strptime(str(tempDate[0]),"%d/%m/%Y")
            created_date=created_date.strftime("%d/%m/%Y")
            tempDate = datetime.datetime.today().strftime("%d/%m/%Y")
            if( created_date == tempDate):
                break
            else:
                continue
        
    cursor.executemany(sqlite_insert_gpu_query,[helper])
    sqliteConnection.commit()
    cursor.close()




def main():
    ScrapingGpus()
    records = RetrieveFromDb()
    CreateAndInsertIntoGpuTables(records)
        

if __name__ == "__main__":

    main()
