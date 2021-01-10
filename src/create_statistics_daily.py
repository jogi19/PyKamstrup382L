import time
import mysql.connector
import datetime
from datetime import *

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
        xtime1 = datetime.strptime(start_value_time,"%Y-%m-%d %H:%M:%S")
        xtime2 = datetime.strptime(str(row[0]),"%Y-%m-%d %H:%M:%S")
        
        xdelta = xtime2.date() - xtime1.date()
        if(xdelta.days>0):
            print(str(xtime1))
            print(str(xtime2))
            print(str(xdelta.days))
            xdelta_energy=float(row[4])-start_value_positive_active_energie
            print(start_value_positive_active_energie)
            print(row[4])
            print(xdelta_energy)
            start_value_positive_active_energie=row[4]
            start_value_time=str(row[0])
            print("to be insert into database:")
            print("timer: "+str(row[0]))
            print("timerzone: "+str(row[1]))
            print("electric_meter_type: "+str(row[2]))
            print("serial_no: "+str(serialnumber))
            print("value_positive_active: "+str(row[4]))
            print("daily_active_energie: "+ str(xdelta_energy))
            #muss wieder raus, wenn es auf der selben Database läuft
            localsqldb = mysql.connector.connect(
                host="localhost",
                user="strom",
                password="power"

            )
            localsqldb.database = "energy_db"
            localcursor = localsqldb.cursor()
            sql = "INSERT INTO daily_power(\
                    time,\
                    timezone,\
                    electric_meter_type,\
                    serial_number,\
                    positive_active_energie,\
                    daily_active_energie)\
                    VALUES \
                    ( \
                    \'"+str(row[0])+"\',\
                    "+str(row[1])+",\
                    \'"+str(row[2])+"\',\
                    "+str(serialnumber)+",\
                    "+str(row[4])+",\
                    "+str(xdelta_energy)+");"
            print(sql)
            localcursor.execute(sql)
            localsqldb.commit()


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
read_from_data(connection,16721739,"2020-12-11 21:50:30",35936.0)
read_from_data(connection,17717664,"2020-12-11 21:47:46",17807.0)

# after initial start use
#start_values_time = get_start_values_time(16721739)
#start_values_energy = get_start_values_energy(16721739)
#read_from_data(connection,16721739,str(start_values_time),float(start_values_energy))

#start_values_time = get_start_values_time(17717664)
#start_values_energy = get_start_values_energy(17717664)
#read_from_data(connection,17717664,str(start_values_time),float(start_values_energy))



17717664