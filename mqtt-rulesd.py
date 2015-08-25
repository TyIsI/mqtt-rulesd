import paho.mqtt.client as mqtt
import json
import os.path
from pprint import pprint

DEBUG = True

def on_connect( client, userdata, flags, rc ):
    print( "Connected" )

    for channel in config['channels']:
        print( "Subscribing to channel: [" + channel + "]" )
        client.subscribe( str( channel ) )

def on_message( client, userdata, msg ):
    check_rules( msg.topic, msg.payload )

def check_rules( address, message ):
    for rule in config['rules']:
        if rule['match']['address'] == address and rule['match']['message'] == message:
            if DEBUG:
                print( "Match for message rule [" + rule['match']['address'] + "/" + rule['match']['message'] + "], pushing message" )
            for dest in rule['push']:
                client.publish( dest['address'], dest['message'] )

if __name__ == "__main__":
    if not os.path.isfile( 'config.json' ):
        die( 'Missing config file config.json' )
    
    with open('config.json') as data_file:
        config = json.load(data_file)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect( config['server']['name'], config['server']['port'], 60 )
    
    client.loop_forever()
