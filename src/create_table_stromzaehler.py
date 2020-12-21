'''
source: https://www.w3schools.com/python/python_mysql_getstarted.asp
This code was just to leran how to handle SQL data base with python
and helped me to create the required databases and tables
I'm not sure if this version creates the correct databases
So, if you find issues, don't hessitate to push fixes :-)
'''

import mysql.connector

def create_database(database):
  mycursor.execute("CREATE DATABASE " + database)

def show_databases():
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)

def create_table(database, table):
  mydb.database = database
  mycursor.execute("CREATE TABLE "+ table+"(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

def create_weather_table(database, table):
  mydb.database = database
  sql = "CREATE TABLE "+ table+"( time DATETIME NOT NULL,\
    datetime DATETIME,\
    timezone INT,\
    electric_meter_type CHAR(64),\
    serial_number INT,\
    positive_active_energie FLOAT,\
    positive_active_energie_tarrif_T1 FLOAT,\
    operating_hour INT,\
    positiv_active_maximum_demand FLOAT,\
    feedin_active_energie FLOAT,\
    feedin_active_energie_tarrif_T1 FLOAT,\
    feeding_active_maximum_demand FLOAT)"
  print(sql)
  mycursor.execute(sql)




def alter_table(database, table):
  mydb.database = database
  mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") 

mydb = mysql.connector.connect(
  host="localhost",
  user="strom",
  password="power"
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE energy_db")
show_databases()
create_weather_table("energy_db","weather_test5")

