import serial
import autopy
arduino = serial.Serial('COM5', 9600)
while True:
    
    
    rawString = arduino.readline()
    rawString_s = rawString.decode()
    

    if rawString_s[0] == 'A':
        width, height = autopy.screen.size()
        width = width/2
        height = height/2
        autopy.mouse.move(width, height)
        print("automatico")

    elif rawString_s[0] == 'M':
        print("manual")

    
arduino.close()