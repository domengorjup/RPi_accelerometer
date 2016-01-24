from time import sleep
import smbus
import numpy as np
import matplotlib.pyplot as plt


# Register addresses 
power_mgmt = 0x6b       # Power management register. Defult is sleep (1), set to 0 to start up!
acc_range = 0x1c        # Acceleroemter range select (0:+-2g; 1:+-4g; 2:+-8g, 3:+-16g)

bus = smbus.SMBus(1)    # MPU-6050 I2C bus on Raspberry Pi
address = 0x68          # MPU-6050 I2C bus address

# Settings:
accelerometer_range = 0     # Select accelerometer range

# Data acquisation functions:

def read_word(adr):
    "Reads and formats 16-bit data from two 8-bit registers."
    high = bus.read_byte_data(address, adr)     # address = device address, adr = register
    low = bus.read_byte_data(address, adr+1)    # low bus address = high bus adderss + 1
    val = (high << 8) + low                     # shift high bus data to first 8 bit
    return val


def read_word_2c(adr):
    "Reads word at adr, decodes it from 16bit 2's format."
    val = read_word(adr)
    if (val >= 0x8000):     # a value higher than 2^15 represents 16 bit complement of negative number
        return -((65535 - val) + 1 )
    else:
        return val          # values < 2^15 are represent themselves


def acc_data(ar=accelerometer_range):
    "continuously reads acceleroemter data, performs basic processing."
    
    acc_x = read_word_2c(0x3b)      # Read data from X-axis registers
    acc_y = read_word_2c(0x3d)      # Read data from Y-axis registers
    acc_z = read_word_2c(0x3f)      # Read data from Z-axis registers

    scale = (16384.0, 8192.0, 4096.0, 2048.0)   # accelerometer sensitivity for range settings [LSB/g]

    x = acc_x / scale[ar]
    y = acc_y / scale[ar]
    z = acc_z / scale[ar]

    x_rotation = get_x_rotation(x,y,z)
    y_rotation = get_y_rotation(x,y,z)

    return (x, y, z, x_rotation, y_rotation)


# Data manipulation functions:

def get_x_rotation(x,y,z):
    "Calculates the angle of rotation about X-axis using accelerometer data."
    rad = np.arctan2(y, np.sqrt(x**2 + z**2))
    return rad / np.pi * 180


def get_y_rotation(x,y,z):
    "Calculates the angle of rotation about Y-axis using accelerometer data."
    rad = np.arctan2(x, np.sqrt(y**2 + z**2))
    return rad / np.pi * 180


if __name__ == "__main__":
    bus.write_byte_data(address, power_mgmt, 0)     # Wake up from sleep
    bus.write_byte_data(address, acc_range, accelerometer_range)    # Set accelerometer range


    while True:
        try:
            (x, y, z, x_rotation, y_rotation) = acc_data()

            print("X rotation:\t{:.3f}".format(x_rotation))
            print("Y rotation:\t{:.3f}\n".format(y_rotation))

            sleep(0.25)
            
        except(KeyboardInterrupt):
            print("Sampling interrupted. Restart to continue.")
            break
