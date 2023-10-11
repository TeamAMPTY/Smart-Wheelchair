import serial

# Define the serial port and baud rate
port = 'COM5'  # Adjust this to match the Arduino's serial port
baud_rate = 9600

try:
    arduino = serial.Serial(port, baud_rate)
except serial.SerialException:
    print(f"Couldn't open port {port}. Check if the Arduino is connected.")
    exit(1)

while True:
    arduino_data = arduino.readline().decode('utf-8').strip()
    if(arduino_data == '0'):
        
    else:
        print(arduino_data)

# Close the serial connection when done (usually when you want to exit the program)
arduino.close()
