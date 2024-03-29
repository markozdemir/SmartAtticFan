# ESP32 Code

This will run every 15 seconds for demonstration purposes. However, in a real time environment, 
the device should go into deepsleep mode, commented out in the infinite while statement, for about 20 minutes.   

Upon starting, the ESP32 will attempt to connect to the internet and send a request to the AWS server. 
If successful, the ESP32 will collect temperature, humidity, and fan RPM on every iteration and send the information to the AWS server.   

Once the server receives the information, the ESP32 will wait to receive the correct fan speed back (3 speed) to turn the fan on to.   

Note: [firmware](https://github.com/markozdemir/SmartAtticFan/tree/main/src/firmware) contains latest esp32 firmware used in development. Feel free to run the shell script under firmware to install.
