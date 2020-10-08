import matplotlib.pyplot as plt
import json_reading


def graph():
    # plot coordinates with lists of humidity and temperature
    # from the json file
    y1_coordinates = json_reading.temp_from_json
    y2_coordinates = json_reading.humid_from_json

    plt.ylabel('Temperature and Humidity')
    plt.xlabel('Recordings in half hour increments')
    plt.plot(y1_coordinates, label="Temperature")
    plt.plot(y2_coordinates, label="Humidity")
    plt.legend()
    plt.show()
