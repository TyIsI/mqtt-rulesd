import paho.mqtt.client as mqtt
import json
import os.path

if not os.path.isfile( 'config.json' ):
    die( 'Missing config file config.json' )

with open('config.json') as data_file:
    config = json.load(data_file)

def on_connect( client, userdata, flags, rc ):
    print( "Connected" )

    print( "Subscribing to channel: [/room1/lamp1]" )
    client.subscribe( '/room1/lamp1' )

def on_message( client, userdata, msg ):
    print( msg.topic + " " + str( msg.payload ) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect( config['server']['name'], config['server']['port'], 60 )

client.loop_forever()
