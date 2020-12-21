import serial

from time import timezone
import time
import mysql.connector
import datetime
import pytz
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB1',parity=serial.PARITY_EVEN,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,baudrate=9600,timeout=1)
ser.write("\x2f\x3f\x21\x0d\x0a")


# feeding values not available yet :-(
#feedin_active_energie FLOAT=""
#feedin_active_energie_tarrif_T1 FLOAT=""
#feeding_active_maximum_demand FLOAT=""

responses = ser.readlines()
type = responses[1]
serial_number = responses[2]
positive_active_energy=responses[3]
positive_active_energy_in_tarrif_T1=responses[4]
betriebsdauer=responses[8]
positive_active_maximum_demand=responses[10]
length = len(responses)
print ("length: " +str(length))
count = 0
for output in responses:
	print ("count: "+str(count)) 
	print(output)
	count = count+1
print('######################')
print('Type                :' +type[1:])
print('Serial Number       :' + serial_number[7:15])
print('Leistung In         :'+positive_active_energy[6:13])
print('Leistung In Tarif T1:'+positive_active_energy_in_tarrif_T1[6:13])
print('Betreibstunden      :'+betriebsdauer[7:14])
print('Maximale Leistung   :'+positive_active_maximum_demand[6:11])


my_datetime=datetime.utcnow()
print("datetime: "+str(my_datetime))
timezone=time.timezone
print("timezone: "+str(timezone))
electric_meter_type=type[1:]
serial_number=serial_number[7:15]
positive_active_energie=positive_active_energy[6:13]
positive_active_energie_tarrif_T1=positive_active_energy_in_tarrif_T1[6:13]
operating_hour=betriebsdauer[7:14]
positiv_active_maximum_demand=positive_active_maximum_demand[6:11]

# feeding values not available yet :-(
#feedin_active_energie FLOAT=""
#feedin_active_energie_tarrif_T1 FLOAT=""
#feeding_active_maximum_demand FLOAT=""

mydb = mysql.connector.connect(
    host="localhost",
    user="strom",
    password="power"
)

mydb.database = "energy_db"
mycursor = mydb.cursor()

sql = "INSERT INTO stromzaehler(\
        time,\
        timezone,\
        electric_meter_type,\
        serial_number,\
        positive_active_energie,\
        positive_active_energie_tarrif_T1,\
        operating_hour,\
        positiv_active_maximum_demand,\
        feedin_active_energie\
        )\
        VALUES \
        ( \
        \'"+str(my_datetime)+"\',\
        "+str(timezone)+",\
        \'"+electric_meter_type+"\',\
        "+serial_number+",\
        "+positive_active_energie+",\
        "+positive_active_energie_tarrif_T1+",\
        "+operating_hour+",\
        "+positiv_active_maximum_demand+",\
         84058);"
print(sql)
mycursor.execute(sql)
mydb.commit()
