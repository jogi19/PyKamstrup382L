import serial
import time

ser = serial.Serial('/dev/ttyUSB1',parity=serial.PARITY_EVEN,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,baudrate=9600,timeout=1)
#ser.write("\x2f\x3f\x21\x0d\x0a")
ser.write(b,'\x2f\x3f\x21\x0d\x0a')

#ser.write("'\x06\x30\x30\x30\x0D\x0A")

responses = ser.readlines()
#type = responses[1]
#serial_number = responses[2]
#positive_active_energy=responses[3]
#positive_active_energy_in_tarrif_T1=responses[4]
#betriebsdauer=responses[8]
#positive_active_maximum_demand=responses[10]
length = len(responses)
print ("length: " +str(length))
count = 0
for output in responses:
	print ("count: "+str(count)) 
	print(output)
	count = count+1
#print('######################')
#print('Type                :' +type[1:])
#print('Serial Number       :' + serial_number[7:15])
#print('Leistung In         :'+positive_active_energy[6:13])
#print('Leistung In Tarif T1:'+positive_active_energy_in_tarrif_T1[6:13])
#print('Betreibstunden      :'+betriebsdauer[7:14])
#print('Maximale Leistung   :'+positive_active_maximum_demand[6:11])


