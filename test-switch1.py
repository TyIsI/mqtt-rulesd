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
    print( "Connected with result code: [" + str( rc ) + "]" )

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    ###print( "Subscribing to channel: [/room1/lamp1]" )
    ###client.subscribe( '/room1/lightswitch1' )

# The callback for when a PUBLISH message is received from the server.
def on_message( client, userdata, msg ):
    print( msg.topic + " " + str( msg.payload ) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect( config['server']['name'], config['server']['port'], 60 )

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
###client.loop_forever()

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
