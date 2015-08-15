import paho.mqtt.client as mqtt
import json
import os.path
from pprint import pprint
from time import sleep

if not os.path.isfile( 'config.json' ):
    die( 'Missing config file config.json' )

with open('config.json') as data_file:
    config = json.load(data_file)

# The callback for when the client receives a CONNACK response from the server.
def on_connect( client, userdata, flags, rc ):
    print( "Connected" )

client = mqtt.Client()

client.connect( config['server']['name'], config['server']['port'], 60 )

client.loop_start()

switch = 0

while True:
    if switch == 0:
        client.publish( '/room1/lightswitch1', 'off' )
        switch = 1
    else:
        client.publish( '/room1/lightswitch1', 'on' )
        switch = 0

    sleep( 5 )
    
client.loop_stop()
