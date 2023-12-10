import os
import serial
import time

baud_rate =115200

def create_serial_connection(port, baud_rate):
    try:
        return serial.Serial(port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

#Function to send commands to GRBL
def send_command(arduino, command):
    if arduino is not None:
        arduino.reset_input_buffer() #Clear the input buffer
        arduino.write(f"{command}\n".encode())
        while True:
            if arduino.in_waiting:
                line = arduino.readline().decode().strip()
                print(line)
                if line == 'ok':
                    break
     #   time.sleep(1) #Give GRBL time to process the command
      #  while arduino.in_waiting:
       #     print(arduino.readline().decode().strip())
    #else:
     #   print("Serial connection not established.") 
        
#Defining Arduino Ports
arduino1_port = "/dev/ttyACM0"
arduino2_port = "/dev/ttyACM1"

arduino_connections = {
    'arduino1' : create_serial_connection(arduino1_port, baud_rate),
    'arduino2' : create_serial_connection(arduino2_port, baud_rate)
    #Add additional modules
}
    
#Defining a mapping from trash types to specific actions
trash_actions = {
    'AluCan': [
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        #...additional actions and moving for sorting for PET
        ],
    'PET': [
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 Z10 F1000', 'timing':3},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y100 F1000', 'timing':4},
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 F1000', 'timing':2},
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 F1000', 'timing':2},
         #...additional actions and moving for sorting for PET
        ],
    'HDPEM': [
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        #...additional actions and moving for sorting for PET
        ],
    'Glass': [
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 X10 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino1', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        {'arduino': 'arduino2', 'command': 'G21 G91 G1 Y10 F1000', 'timing':2},
        #...additional actions and moving for sorting for PET
        ],

    #Define actions for other types of trash
}

def perform_actions(trash_type):
    actions = trash_actions.get(trash_type, [])
    last_arduino = None
    for action in actions:
        arduino = arduino_connections.get(action['arduino'])
        if arduino:
            if last_arduino == arduino:
                time.sleep(1) #Adjust this delay as needed
            send_command(arduino, action['command'])
            time.sleep(action['timing']) #wait for the action to complete
        last_arduino = arduino

def reset_serial_connection(arduino):
    arduino.close()
    time.sleep(0.5) #Short delay to ensure the port is closed properly
    arduino.open()
#Main Loop
while True:
    with open('temp_output.txt', 'r') as file:
        trash_type = file.readline().strip()
        print(trash_type)
        time.sleep(2)
    #trash_type = input("Enter trash type (or 'q' to quit):").strip()
    if trash_type.lower() == 'q':
        break
    perform_actions(trash_type)
    #Reset serial connections
    for arduino in arduino_connections.values():
        if arduino:
            reset_serial_connection(arduino)
    
    break
  
#cleanup: close all serial connections
for ser in arduino_connections.values():
    if ser:
        ser.close()
