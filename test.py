import time
import requests
import json
def ma():
  s='https://t-adder-app-clients-default-rtdb.firebaseio.com/.json'
  i=1
  while(True):
   requests.patch(s,json={'y':i})
   i+=1
   time.sleep(2)
ma()
  
