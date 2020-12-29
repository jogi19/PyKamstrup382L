import time
import mysql.connector
import datetime
from datetime import *

start_value_serial=16721739
    

def create_connection(db_file):
    """ 
    create a database connection energy_db
    on 192.168.178.33
    """
    mysqldb = mysql.connector.connect(
          host="192.168.178.33",
          user="grafana",
          password="grafana",
          db=db_file
        )
    return mysqldb
    
def read_from_data(mysqldb,serialnumber,starttime=0,start_value_positive_active_energie=0):
    '''
    read all data from a certain date
    '''
    start_value_time=starttime
    #start_value_positive_active_energie=35936.0
    #mysqldb.database = db_file
    dbcursor = mysqldb.cursor()
    sql = "SELECT * FROM stromzaehler WHERE( time>\'"+str(starttime)+"\' AND serial_number="+str(serialnumber)+")"
    #print(sql)
    
    dbcursor.execute(sql)
    rows = dbcursor.fetchall()
    for row in rows:
        #print(str(row))
        #print(row[0])
        #print(row[4])
        if(row[4]>start_value_positive_active_energie):
            average_power =calculate_average_power(start_value_positive_active_energie, row[4], start_value_time,str(row[0]))
            print("to be insert into database:")
            print("timer: "+str(row[0]))
            print("timerzone: "+str(row[1]))
            print("electric_meter_type: "+str(row[2]))
            print("serial_no: "+str(serialnumber))
            print("value_positive_active: "+str(row[4]))
            print("average power: "+ str(average_power))
            #muss wieder raus, wenn es auf der selben Database läuft
            localsqldb = mysql.connector.connect(
                host="localhost",
                user="strom",
                password="power"

            )
            localsqldb.database = "energy_db"
            localcursor = localsqldb.cursor()
            sql = "INSERT INTO average_power_in(\
                    time,\
                    timezone,\
                    electric_meter_type,\
                    serial_number,\
                    positive_active_energie,\
                    average_active_energie)\
                    VALUES \
                    ( \
                    \'"+str(row[0])+"\',\
                    "+str(row[1])+",\
                    \'"+str(row[2])+"\',\
                    "+str(serialnumber)+",\
                    "+str(row[4])+",\
                    "+str(average_power)+");"
            print(sql)
            localcursor.execute(sql)
            localsqldb.commit()
            start_value_positive_active_energie=row[4]
            start_value_time=str(row[0])

def calculate_average_power(old_P, new_P, old_time,new_time):
    print("########## calculate_average_power #############")
    print("old_P: "+str(old_P))
    print("new_P: "+str(new_P))
    print("old_time: "+old_time)
    print("new_time: "+new_time)
    time1 = datetime.strptime(old_time,"%Y-%m-%d %H:%M:%S")
    time2 = datetime.strptime(new_time,"%Y-%m-%d %H:%M:%S")
    delta=time2-time1
    print("Delta: "+str(delta.seconds))
    average_power=(new_P-old_P)*3600*1000/(delta.seconds)
    print("average_power: "+ str(average_power))
    return average_power

def get_start_values_energy(serialnumber):
    positive_active_energie = 0
    sql = "SELECT MAX(positive_active_energie) FROM average_power_in WHERE serial_number="+str(serialnumber)+";"
    localsqldb = mysql.connector.connect(
        host="localhost",
        user="strom",
        password="power"

        )
    localsqldb.database = "energy_db"
    localcursor = localsqldb.cursor()
    print(sql)
    localcursor.execute(sql)
    rows = localcursor.fetchall()
    for row in rows:
        positive_active_energie = row[0]
    
    print("positive_active_energie: "+ str(positive_active_energie))
    return positive_active_energie

def get_start_values_time(serialnumber):
    time = ""
    sql = "SELECT MAX(time) FROM average_power_in WHERE serial_number="+str(serialnumber)+";"
    localsqldb = mysql.connector.connect(
        host="localhost",
        user="strom",
        password="power"

        )
    localsqldb.database = "energy_db"
    localcursor = localsqldb.cursor()
    print(sql)
    localcursor.execute(sql)
    rows = localcursor.fetchall()
    for row in rows:
        time = row[0]
    
    print("time: "+ str(time))
    return time


connection = create_connection("energy_db")
# first start ....
#read_from_data(connection,16721739,"2020-12-11 21:50:30",35936.0)
#read_from_data(connection,17717664,"2020-12-11 21:47:46",17807.0)

# after initial start use
start_values_time = get_start_values_time(16721739)
start_values_energy = get_start_values_energy(16721739)
read_from_data(connection,16721739,str(start_values_time),float(start_values_energy))

start_values_time = get_start_values_time(17717664)
start_values_energy = get_start_values_energy(17717664)
read_from_data(connection,17717664,str(start_values_time),float(start_values_energy))



