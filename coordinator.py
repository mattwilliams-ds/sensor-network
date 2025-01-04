# Coordinator
# M. Williams - SIE559

import xbee, time

# Check & clear cached messages
received_msg = xbee.receive()
while received_msg:
    received_msg = xbee.receive()

print('\n\n--------------------------')
print('Waiting to receive data...')

while True:
    received_msg = xbee.receive()                             # check for received messages

    if received_msg:
        sender = received_msg['sender_eui64']                 # store sender's address
        message = received_msg['payload']                     # store message received
        print(message.decode())                               # print decoded message to serial port

    time.sleep(0.25)                                          # pause for 1/4 seconds & run again
