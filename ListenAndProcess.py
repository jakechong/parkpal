import requests
import json
import time
import datetime

delay = 1*30 # Delay in seconds

base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}

# Run once at the start
def setup():
    try:
        query = {
            'stream-name': 'Parking Spot 1',
            'points-type': 'i' # 'i', 'f', or 's'
        }
        endpoint = '/networks/'+network_id+'/objects/arduino-uno/streams/parking-spot1'
        response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        if resp['stream-code'] == 201:
            print('Create stream parking-spot1: ok')
        else:
            print('Create stream parking-spot1: error')
            print( response.text )
            
        query0 = {
            'stream-name': 'Parking Spot 2',
            'points-type': 'i' # 'i', 'f', or 's'
        }
        endpoint0 = '/networks/'+network_id+'/objects/arduino-uno/streams/parking-spot2'
        response0 = requests.request('PUT', base + endpoint0, params=query0, headers=header, timeout=120 )
        resp0 = json.loads( response0.text )
        if resp0['stream-code'] == 201:
            print('Create stream parking-spot1: ok')
        else:
            print('Create stream parking-spot1: error')
            print( response0.text )
    except:
        print "Setup Error"

# Run continuously forever
def loop():
    #  Read points from stream 1 (sensor1)
    endpoint1 = '/networks/local/objects/arduino-uno/streams/sensor1/points'
    query1 = {'points-limit': 3}
    response1 = requests.request('GET', base + endpoint1, params=query1, headers=header, timeout=120 )
    resp1 = json.loads( response1.text )
    if resp1['points-code'] == 200:
        print( 'Read sensor1 points: ok')
    else:
        print( 'Read sensor1 points: error')
        print( response1.text )
    #  Read points from stream 2 (sensor2)
    endpoint2 = '/networks/local/objects/arduino-uno/streams/sensor2/points'
    query2 = {'points-limit': 3}
    response2 = requests.request('GET', base + endpoint2, params=query2, headers=header, timeout=120 )
    resp2 = json.loads( response2.text )
    if resp2['points-code'] == 200:
        print( 'Read sensor2 points: ok')
    else:
        print( 'Read sensor2 points: error')
        print( response2.text )
    #Take average of the last 3 readings (last 30 seconds) for sensor 1
    s1_sum = 0
    for s1_points in resp1['points']:
        s1_sum += s1_points['value']
    avg_s1 = s1_sum/3
    #Take average of the last 3 readings (last 30 seconds) for sensor 2
    s2_sum = 0
    for s2_points in resp2['points']:
        s2_sum += s2_points['value']
    avg_s2 = s2_sum/3
    #Determine car presence based of average readings
    if avg_s1 > 0.5: #when the sensor reads there's a car more than 50% of the time
        parking_spot1 = 1 # 1 means that the spot is available = 1 spot(s) available
    else:
        parking_spot1 = 0 # 0 means that the spot is taken = O spot(s) available
    if avg_s2 > 0.5:
        parking_spot2 = 1
    else:
        parking_spot2 = 0
    # Post point to stream 3 (parking-spot1)  
    endpoint3 = '/networks/local/objects/arduino-uno/streams/parking-spot1/points'
    query3 = {
        'points-value': parking_spot1,
        'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    response3 = requests.request('POST', base + endpoint3, params=query3, headers=header, timeout=120 )
    resp3 = json.loads( response3.text )
    if resp3['points-code'] == 200:
        print( 'Update parking-spot1 points: ok')
    else:
        print( 'Update parking-spot1 points: error')
        print( response3.text )
     # Post point to stream 4 (parking-spot2)  
    endpoint4 = '/networks/local/objects/arduino-uno/streams/parking-spot2/points'
    query4 = {
        'points-value': parking_spot2,
        'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    response4 = requests.request('POST', base + endpoint4, params=query4, headers=header, timeout=120 )
    resp4 = json.loads( response4.text )
    if resp4['points-code'] == 200:
        print( 'Update parking-spot2 points: ok')
    else:
        print( 'Update parking-spot2 points: error')
        print( response4.text )
    # 30 seconds delay
    time.sleep(30)
    return

# Run continuously forever
# with a delay between calls
def delayed_loop():
    print "Delayed Loop"

# Run once at the end
def close():
    try:
        print "Close"
    except:
        print "Close Error"
    
# Program Structure    
def main():
    # Call setup function
    setup()
    print("Start reading and processing points (Ctrl+C to stop)")
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