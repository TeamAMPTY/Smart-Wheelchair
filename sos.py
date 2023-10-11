from twilio.rest import Client
import serial

client = Client('ACf279eb9fc582f4cbc5911f45ed68579a','fcfd1f20f35d634b89af7536f1822284')

def sendMsg():
    message = client.messages.create(
    body='The patient had fallen down! Rescue Fast...',
    from_='+12565983954',
    to='+917457880121'
)


port = 'COM5' 
baud_rate = 9600

try:
    arduino = serial.Serial(port, baud_rate)
except serial.SerialException:
    print(f"Couldn't open port {port}. Check if the Arduino is connected.")
    exit(1)

while True:
    arduino_data = arduino.readline().decode('utf-8').strip()
    if(arduino_data == '0'):
        sendMsg()
        break;
    else:
        print(arduino_data)
