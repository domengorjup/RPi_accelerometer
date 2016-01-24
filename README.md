A test project using python 3 in a Raspberry Pi 2 B to read accelerometer  data from a MPU-6050 chip.  
The accelerometer data is hosted on local network using Flask.  
Data acquisation part of this project roughly follows [Bitify's guide found here](http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html).  


Dependencies: 
- [Python 3](https://www.python.org/downloads/)
- [NumPy](http://www.numpy.org)
- [Flask](http://flask.pocoo.org) web framework
- smbus module for I2C communication (`sudo apt-get install python3-smbus`)

