# This program subscribe the message of nodes in the mesh network. The received message is saved in a text file with node id. The message starts with painless/from/12345678"
# where 12345678 is the node id of the node that has sent the message. The message includes the node name, Analog reading of pin A0 of ESP8266 and free memory present
# in ESP8266. Please enter the Local ip address of your PC/Laptop in the line with "****"
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
import csv
import os 
import socket

currentFile    =   __file__                      #The full path and filename of the file  
realPath       =   os.path.realpath(currentFile) #file full path with filename
dirPath        =   os.path.dirname(realPath)
if not os.path.exists(dirPath+"/data/"):
            os.makedirs(dirPath+"/data/") 
host           =   socket.gethostname()  
filename= dirPath+"/data/"+datetime.now().strftime('%d-%m-%y')+"_"+host+"_data"+".csv"
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) #Print result of connection attempt
    client.subscribe("hetadatainMesh/from/+")    # Subscribe all msg having topic "painlessMesh/from/"
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")     

def on_message(client, userdata, msg):

    f = open(filename, "a") 
    msg.payload = msg.payload.decode("utf-8")
    if msg.payload == "ready":
        client.publish("hetadatainMesh/to/gateway", "subready")
    #Print a received msg
    print(datetime.now().strftime('%d-%m-%y %H:%M:%S') + "," + str(msg.payload)+"\n", file = f)
    print(datetime.now().strftime('%H:%M:%S') + "," + str(msg.payload))
    #print(datetime.fromtimestamp(ts_epoch, timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + "," + str(msg.payload) +"\n", file = f)
    #print(datetime.fromtimestamp(ts_epoch, timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + "," + str(msg.payload)) 



client = mqtt.Client()               # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect       # Define callback function for successful connection
client.on_disconnect = on_disconnect # Define callback function for disconnection
client.on_message = on_message       # Define callback function for receipt of a message
client.username_pw_set("username", "password")
client.connect("50.62.22.142", 1883, 100)
client.loop_forever()


