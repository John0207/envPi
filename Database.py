import pyrebase
import datetime as DT
from firebase_admin import storage


config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "serviceAccount": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

storage = firebase.storage()


def add_data_file_to_storage():
    storage.child("data/data.json").put("data.json")


def time_stamp():
    ts = DT.datetime.now()
    st = ts.strftime('%Y-%m-%d %H:%M')
    return st


def send_data_to_firebase(temp_string, humid_string, light_sensor_value):
    # For firebase database
    db.child("data").push({
        'fTemp': temp_string,
        'humidity': humid_string,
        'light': light_sensor_value,
        'time': time_stamp()
    })


def send_settings_to_firebase(too_low_temp, just_right_temp, too_high_temp, humidity_limit, light_threshold):
    db.child("settings").set({
        'too low': too_low_temp,
        'just right': just_right_temp,
        'too hot': too_high_temp,
        'humidity limit': humidity_limit,
        'light threshold': light_threshold
    })


def print_data_confirmation(temp_string, humid_string):
    print("Temp:" + temp_string + "F\n" + "Humidity :" + humid_string + "%")
    print("This data was recorded!\n")


def get_low_temp():
    low_temp = db.child('settings').child('too low').get().val()
    return low_temp


def get_high_temp():
    high_temp = db.child('settings').child('too hot').get().val()
    return high_temp


def get_just_right_temp():
    just_right_temp = db.child('settings').child('just right').get().val()
    return just_right_temp


def get_humidity_limit():
    humidity_limit = db.child('settings').child('humidity limit').get().val()
    return humidity_limit


def get_light_threshold():
    light_threshold = db.child('settings').child('light threshold').get().val()
    return light_threshold


