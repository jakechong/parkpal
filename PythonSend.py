import serial
# Change the port name to match the port # to which your Arduino is connected.
serial_port_name = '/dev/cu.usbmodem1411' # for Mac
ser = serial.Serial(serial_port_name, 9600, timeout=1)

import requests
import json
import time
import datetime

delay = 1*5 # Delay in seconds

base = 'http://ucbparkpal.herokuapp.com'
network_id = 'local'
header = {}
        
# Run once at the start
def setup():
    try:
        query1 = {
            'object-name': 'Arduino Uno'
        }
        endpoint1 = '/networks/'+network_id+'/objects/arduino-uno'
        response1 = requests.request('PUT', base + endpoint1, params=query1, headers=header, timeout=120 )
        resp1 = json.loads( response1.text )
        if resp1['object-code'] == 201:
            print('Create object arduino-uno: ok')
        else:
            print('Create object arduino-uno: error')
            print( response1.text )
            
        query2 = {
            'stream-name': 'Sensor 1',
            'points-type': 'i' # 'i', 'f', or 's'
        }
        endpoint2 = '/networks/'+network_id+'/objects/arduino-uno/streams/sensor1'
        response2 = requests.request('PUT', base + endpoint2, params=query2, headers=header, timeout=120 )
        resp2 = json.loads( response2.text )
        if resp2['stream-code'] == 201:
            print('Create stream sensor 1: ok')
        else:
            print('Create stream sensor 1: error')
            print( response2.text )
            
        query3 = {
            'stream-name': 'Sensor 2',
            'points-type': 'i' # 'i', 'f', or 's'
        }
        endpoint3 = '/networks/'+network_id+'/objects/arduino-uno/streams/sensor2'
        response3 = requests.request('PUT', base + endpoint3, params=query3, headers=header, timeout=120 )
        resp3 = json.loads( response3.text )
        if resp3['stream-code'] == 201:
            print('Create stream sensor 2: ok')
        else:
            print('Create stream sensor 2: error')
            print( response3.text )
    except:
        print "Setup Error"

# Run continuously forever
def loop():
    # Check if something is in serial buffer
    if ser.inWaiting() > 0:
        try:
            # Read entire line - (Receive Point 1)
            x = ser.readline()
            print "Received:", x
            # Read entire line - (Receive Point 2)
            y = ser.readline()
            print "Received:", y
            # Create endpoints for the 2 different streams
            endpoint1 = '/networks/local/objects/arduino-uno/streams/sensor1/points'
            endpoint2 = '/networks/local/objects/arduino-uno/streams/sensor2/points'
            # Post point to stream 1
            query = {
                'points-value': int(x), #convert from string to integer
                'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            response1 = requests.request('POST', base + endpoint1, params=query, headers=header, timeout=120 )
            resp1 = json.loads( response1.text )
            if resp1['points-code'] == 200:
                print( 'Update sensor 1 points: ok')
            else:
                print( 'Update sensor 1 points: error')
                print( response1.text )
            # Post point to stream 2    
            query = {
                'points-value': int(y), #convert from string to integer
                'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            response2 = requests.request('POST', base + endpoint2, params=query, headers=header, timeout=120 )
            resp2 = json.loads( response2.text )
            if resp2['points-code'] == 200:
                print( 'Update sensor 2 points: ok')
            else:
                print( 'Update sensor 2 points: error')
                print( response2.text )
        except:
            print "Error"
            
    # 100 ms delay
    time.sleep(0.1)
    return

# Run once at the end
def close():
    try:
        print "Close Serial Port"
        ser.close()
    except:
        print "Close Error"
    
# Program Structure    
def main():
    # Call setup function
    setup()
    print("Start sending points (Ctrl+C to stop)")
    while(True):
        # Try loop() and delayed_loop()
        try:
            loop()
        except KeyboardInterrupt:
            # If user enters "Ctrl + C", break while loop
            break
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()