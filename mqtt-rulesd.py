import paho.mqtt.client as mqtt
import json
import os.path
from pprint import pprint

if not os.path.isfile( 'config.json' ):
    die( 'Missing config file config.json' )

with open('config.json') as data_file:
    config = json.load(data_file)

def on_connect( client, userdata, flags, rc ):
    print( "Connected" )

    for channel in config['channels']:
        print( "Subscribing to channel: [" + channel + "]" )
        client.subscribe( str( channel ) )

def on_message( client, userdata, msg ):
    check_rules( msg.topic, msg.payload )

def check_rules( topic, payload ):
    for rule in config['rules']:
        if rule['source'] == topic and rule['match'] == payload:
            print( "Match for message rule [" + rule['source'] + "/" + rule['match'] + "], pushing message" )
            client.publish( rule['destination'], rule['push'] )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect( config['server']['name'], config['server']['port'], 60 )

client.loop_forever()
