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
          password="grafana"
          
        )
    return mysqldb
    
def read_from_data(mysqldb,db_file,serialnumber,starttime=0):
    '''
    read all data from a certain date
    '''
    start_value_time="2020-12-11 21:50:30"
    #start_value_positive_active_energie=35936.0
    start_value_positive_active_energie=0
    mysqldb.database = db_file
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
            print("serial_no: "+str(serialnumber))
            print("average power: "+ str(average_power))
            print("value_positive_active: "+str(row[4]))
            
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




connection = create_connection("energy_db")
read_from_data(connection,"energy_db",16721739,"2020-12-11 21:50:30")
#read_from_data(connection,"energy_db",16721739,"0")
read_from_data(connection,"energy_db",17717664,"2020-12-11 21:50:30")