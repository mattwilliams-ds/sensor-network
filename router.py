# Router Script
# M. Williams - SIE559

import machine
import xbee, time

def ping(node):
    # A function for finding a node & its address
    num_node = 0
    print('Looking for a node to transmit to...')

    while num_node < 1:                                       # check for a node every 10s until one is found
        try:                                                  # try discovering nearby nodes
            for i in xbee.discover():
                if i['node_id'] == node:                      # check node ID
                    num_node += 1
                    address = i['sender_eui64']               # save node address
                    print('Node found!')
            if num_node == 0:
                print('Still looking...')
                time.sleep(5)                                 # sleep for 10s if no node is found
        except:                                                       # this except clause restarts the while loop ->
            print('Waiting for receiving node to start operating...') #   in hte event of an OSERROR
            time.sleep(5)
    return [address]

def measure():
    # A function for taking a sensor measurement
    new_measurement = sm_sensor.read()
    pct_humidity = round(new_measurement / 4095 * 100, 2)     # convert raw data to % humidity & round to 2 decimal places
    return pct_humidity

def send(address, message):
    # A function used to send messages
    xbee.transmit(address, message)                           # send message to receiving node
    return

def check_messages():
    # A function to check messages & forward to coordinator
    received_msg = xbee.receive()                             # check for messages from end node
    if received_msg:
        #sender = received_msg['sender_eui64']                # store sender's address
        in_message = received_msg['payload']                  # store message received
        status = 'Data received: "%s"' % in_message.decode()  # create response
        print(status)
        send(coord_address[0], str(in_message.decode()))      # forward received data
    return

# Check & clear cached messages
received_msg = xbee.receive()
while received_msg:
    received_msg = xbee.receive()

sm_sensor = machine.ADC('D3')                                 # setup soil moisture sensor on A03
plant_id = 'pothos_01'                                        # set plant ID
coord_address = ping('coordinator')                           # find address of the coordinator

# main loop
while True:
    try:
        check_messages()                                      # check for messages from end node & forward to coordinator

        data = measure()                                      # measure soil moisture
        message = plant_id + ',' + str(data)                  # concatenate sensor ID with data
        send(coord_address[0], message)                       # transmit data
        print('Soil Moisture: ', data)

        time.sleep(5)                                         # pause for 5s
    except:
        print('Lost connection, reconnecting...')
        coord_address = ping('coordinator')                   # ping connecting node again if connection is lost
