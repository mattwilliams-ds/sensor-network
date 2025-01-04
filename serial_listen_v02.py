# A script for listening and recording data received over a serial port
#
# Note: the serial library required is installed via pyserial, not serial
#

import time, serial

def write_data(filename, output):
    # A function to write data to a text file
    datafile = open(filename,'a')                              # open outputfile to append data
    datafile.writelines(output)                                # write arduino data to text file
    datafile.close()
    return output

# Setup port to listen to Arduino
arduino_port = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600)                                           # must match baud set in arduino code

# Setup USB port to listen to XBee coordinator
xbee_port = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600)                                           # must match baud set in arduino code

# Initialize a new CSV file for recording data
filename = 'newdata.csv'
datafile = open(filename,'w')
datafile.close()

# Print updates to terminal
print('New data file initialized.')
print('Waiting for data...')

# Main loop to listen, process and write data received
while True:
    # Read serial ports of XBee Coordinator & Arduino
    xbee_data = xbee_port.readline().decode()
    arduino_data = arduino_port.readline().splitlines()[0].decode()

    # Create a timestamp
    timestamp = time.strftime('%x,%X')

    # Append received data to timestamp
    arduino_write = timestamp + ',' + arduino_data.partition('\r')[0] + '\n'
    xbee_write = timestamp + ',' + xbee_data.partition('\r')[0] + '\n'

    # Write data to text file
    write_data(filename, arduino_write)
    write_data(filename, xbee_write)

    # Print write data to terminal for live monitoring
    print(arduino_write)
    print(xbee_write)


