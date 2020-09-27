'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# imports needed to communicate with firebase, as well as to work with the grovepi.
# libraries also needed for exceptions, time for the while loop, and to work with json.
import ts as ts
from firebase_admin import db
import grovepi
from grove_rgb_lcd import setRGB, setText_norefresh, setText
from time import sleep
from math import isnan
import json
import pyrebase
import datetime as DT

config = {"This is where configuration data goes for Firebase"}

firebase = pyrebase.initialize_app(config)

# set ports for light and dht sensors, lcd uses I2c port
# connect light sensor to port A0
light_sensor = 0
# connect the DHt sensor to port 7
dht_sensor_port = 7
# use 0 for the blue-colored sensor and 1 for the white-colored sensor
dht_sensor_type = 0

# set white as backlight color
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(255, 255, 255)

# Take sensor data every 30 minutes to align with graph
time_to_sleep_half_hour = .5 * 60 * 60

# Take sensor data every 3 seconds for testing
time_to_sleep_short = 3

# temperature limits in f:
# Lower limit
too_low_temp = 60.0
# Perfect Temp
just_right_temp = 30.0
# Temp Too high
too_high_temp = 95.0

# Humidity Limit
humidity_limit = 60.0

# light_threshold, good value for light/dark room
# should be adjusted for each room system is in
light_threshold = 57

# Get a reference to the database service
db = firebase.database()


def time_stamp():
    ts = DT.datetime.now()
    st = ts.strftime('%Y-%m-%d %H:%M:%S')
    return st


# boolean functions to determine state of the environment
def warm():
    if (temp_int > just_right_temp) and (temp_int < too_high_temp) and (humid_int < humidity_limit):
        return True
    else:
        return False


def comfortable():
    if (temp_int >= too_low_temp) and (temp_int <= just_right_temp) and (humid_int < humidity_limit):
        return True
    else:
        return False


def too_hot():
    if temp_int >= too_high_temp:
        return True
    else:
        return False


def too_humid():
    if humid_int >= humidity_limit:
        return True
    else:
        return False


def comfortable():
    if (temp_int >= too_low_temp) and (temp_int <= just_right_temp) and (humid_int < humidity_limit):
        return True
    else:
        return False


def too_cold():
    if temp_int <= too_low_temp:
        return True
    else:
        return False


# Function to determine the background color of the lcd screen
def calculate_lcd_background_color(temp_int, humid_int):
    # initialize the color array
    background_color_list = [0, 0, 0]
    # green for comfortable conditions
    if comfortable():
        r = 0
        g = 255
        b = 0
    # orange for warm conditions
    elif warm():
        r = 255
        g = 62
        b = 0
    # green/blue for too humid
    elif too_humid():
        r = 0
        g = 255
        b = 128
    # red for too hot
    elif too_hot():
        r = 255
        g = 0
        b = 0
    # blue for too cold
    elif too_cold():
        r = 0
        g = 0
        b = 255

    # build list of color values to return
    background_color_list = [r, g, b]
    return background_color_list


# Function for converting Celsius to Fahrenheit
def celsius_to_fahrenheit(tempc):
    tempf = round((tempc * 1.8) + 32, 2)
    return tempf


# function which stores data from sensors into file
def append_data_to_file(temp_int, humid_int):
    data_file_list.append([temp_int, humid_int])
    with open("data.json", "w") as write_file:
        json.dumps(data_file_list, write_file)


def print_data_confirmation():
    print("Temp:" + temp_string + "F\n" + "Humidity :" + humid_string + "%")
    print("This data was recorded!\n")


def print_light_value():
    global light_sensor_value
    # set light sensor value variable
    light_sensor_value = grovepi.analogRead(light_sensor)
    # print results to console
    print("sensor_value = %d\n" % light_sensor_value)


def send_data_to_firebase():
    # For firebase database
    db.child(time_stamp()).set({
        'fTemp': temp_string,
        'humidity': humid_string
    })


# create data file list to store data just before while loop
data_file_list = []
# Main loop
while True:
    try:
        # print the light value for configuration of the system
        print_light_value()

        # get the temperature and humidity from the DHT sensor, store in list
        [temp, hum] = grovepi.dht(dht_sensor_port, dht_sensor_type)

        # use conversion function to convert temp from sensor to F and store in variable
        fahrenheit = celsius_to_fahrenheit(temp)

        # convert temp and humid to strings
        temp_string = str(fahrenheit)
        humid_string = str(hum)

        # convert temp in F and humidity to int
        temp_int = int(fahrenheit)
        humid_int = int(hum)

        # if light sensor value is under light_threshold, display message to console
        if light_sensor_value < light_threshold:
            print("Insufficient Light - No Data Recorded\n")

        # if light sensor value is over light_threshold, write data to json file
        # print values to console and change background color of the lcd accordingly
        elif light_sensor_value > light_threshold:
            # send data to json file and firebase database
            append_data_to_file(temp_int, humid_int)
            send_data_to_firebase()
            # calculate lcd color
            background_color_list = calculate_lcd_background_color(temp_int, humid_int)
            # set lcd color
            setRGB(background_color_list[0], background_color_list[1], background_color_list[2])
            # print data/confirmation to the console
            print_data_confirmation()

        # check if we have nans
        # if so, then raise a type error exception
        if isnan(temp) is True or isnan(hum) is True:
            raise TypeError('nan error')

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
        # set text of the lcd screen to display readings
        setText_norefresh("Temp:" + temp_string + "F\n" + "Humidity :" + humid_string + "%")

        # wait before executing loop again
        sleep(time_to_sleep_short)

    except (IOError, TypeError) as e:
        print(str(e))
        # since we got a type error
        # reset the LCD's text
        setText("")

    except KeyboardInterrupt as e:
        print(str(e))
        # since we're exiting the program
        # it's better to leave the LCD with a blank text
        setText("")
        # turn off backlight
        setRGB(0, 0, 0)
        break
