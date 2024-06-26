import pandas as pd
import datetime
import serial
import time
import signal
import sys

people = 0
increment = 0

def signal_handler(sig, frame):
    print('Received termination signal. Exiting gracefully.')
    # Perform any cleanup or finalization here
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def people_count(people: int, increment: int) -> int:
  people += increment
  return people

def capacity_calc(people:int) -> str:
  #return str(people)
   if people <= 50:
     return 'Low Capacity'
   elif people > 50 and people <= 100:
     return 'Medium Capacity'
   elif people > 100 and people <= 150:
     return 'High Capacity'
   else:
     return 'Packed'

def get_time() -> str:
  now = datetime.datetime.now() 
  if now.hour == 0:
    standard_hour = 12
    AM_PM = 'AM'
  elif now.hour > 12:
    standard_hour = now.hour - 12
    AM_PM = 'PM'
  elif now.hour == 12:
    standard_hour = 12
    AM_PM = 'PM'
  else:
    standard_hour = now.hour
    AM_PM = 'AM'

  if now.minute < 10:
    standard_minute = '0' + str(now.minute)
  else:
     standard_minute = str(now.minute)

  return str(standard_hour) + ':' + standard_minute + AM_PM

ser = serial.Serial('/dev/tty.usbmodem143301', 9600)

try:
    while True:
      increment=0
      if ser.in_waiting !=0:
        increment = int(ser.readline().decode('utf-8'.rstrip()))
      
      if(people ==0 and increment == -1):
        increment=0

      people = people_count(people, increment)

      #people = 100 #test number, variable 'people' will show current count

      capacity = capacity_calc(people)

      current_time = get_time()

      data = {
        "Frank Dining Hall" : {"Count": people, "Capacity": capacity, "Last Update":str(current_time)},
        #"Coop" : {"Capacity": capacity, "Last Update":str(current_time)},
        # "Location": ["Frank Dining Hall"],
        # "Capacity": [capacity],
        # "LastUpdate": [str(current_time)],
        # f"{current_time}": [capacity],

      }
      dataframe = pd.DataFrame(data).transpose()

      dataframe.to_csv("/Users/dankim/Documents/CodeGate2024/Frankfully/congregate/src/main/resources/data/df.csv")
except KeyboardInterrupt:
    print("KeyboardInterrupt received. Exiting.")
    sys.exit(0)

  #print(dataframe) 
