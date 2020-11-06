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

from math import isnan
from time import sleep

# imports needed to communicate with the grovepi.
# libraries also needed for exceptions, time for the while loop, and to work with json and the database.
import grovepi
from grove_rgb_lcd import setRGB, setText_norefresh, setText
import Database
import json
import Menu

# set the settings here
Database.send_settings_to_firebase(too_low_temp=80, just_right_temp=90, too_high_temp=95, humidity_limit=60,
                                   light_threshold=57)
# Run the menu function here so that the user's choices are written to the variables
Menu.menu()

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
too_low_temp = Database.get_low_temp()
# Perfect Temp
just_right_temp = Database.get_just_right_temp()
# Temp Too high
too_high_temp = Database.get_high_temp()

# Humidity Limit
humidity_limit = Database.get_humidity_limit()

# light_threshold, good value for light/dark room
# should be adjusted for each room system is in
light_threshold = Database.get_light_threshold()


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
    if too_humid():
        r = 0
        g = 255
        b = 128
    elif comfortable():
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


# print value from light sensor to console
def print_light_value():
    print("sensor_value = %d\n" % light_sensor_value)


def append_data_to_json_file():
    data_file_list.append([Database.get_last_temp(), Database.get_last_humidity()])
    with open("data.json", "w") as write_file:
        json.dump(data_file_list, write_file)


# create data file list to store data just before while loop
# this is written to a json file which is used to draw the graph
data_file_list = []

# Main loop
while True:
    try:
        # read the light sensor value from the sensor
        light_sensor_value = grovepi.analogRead(light_sensor)

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
            print("\nInsufficient Light - No Data Recorded\n")

        # if light sensor value is over light_threshold, write data to json file
        # print values to console and change background color of the lcd accordingly
        elif light_sensor_value > light_threshold:
            # send data to json file and firebase database
            append_data_to_json_file()
            # send recordings from the sensors to Firebase database
            Database.send_data_to_firebase(temp_string, humid_string, light_sensor_value)
            # calculate lcd color
            background_color_list = calculate_lcd_background_color(temp_int, humid_int)
            # set lcd color
            setRGB(background_color_list[0], background_color_list[1], background_color_list[2])
            # print data/confirmation to the console
            Database.print_data_confirmation(temp_string, humid_string)
            # update database with most recent temp and humidity values
            Database.update_latest_entry(temp_int, humid_int)

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
        # exit message since keyboard interrupt is the most efficient way to end the program
        print("GoodBye :)")
        # since we're exiting the program
        # it's better to leave the LCD with a blank text
        setText("")
        # turn off backlight
        setRGB(0, 0, 0)
        break
