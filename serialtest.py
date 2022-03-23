import serial
import time
#from psychopy import parallel

def main():
    # open the port
    
    port = serial.Serial("COM4", 9600, bytesize=serial.EIGHTBITS)
    #port.open()
    for i in range(15):
        port.write(b'111')
        port.write(b'0')
        port.write(b'111')
        port.write(b'0')
    port.close()
    return 0


main()