import serial
def send(trash):
    while True:
        ser = serial.Serial('/dev/ttyAMA0', 9600)
        ser.write(trash.encode())
        print("Sending")
        
    ser.close()
        
    
    return 0


send("hello")