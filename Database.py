import pyrebase
import datetime as DT

# enter credentials from Firebase project here
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
# Initialize Firebase database and create a reference
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# used to create timestamp which is saved with each entry
def time_stamp():
    ts = DT.datetime.now()
    st = ts.strftime('%Y-%m-%d %H:%M:%S')
    return st


# used to update the "last" branch of the database
# the "last" branch stores only the latest temperature and humidity values
def update_latest_entry(temp_string, humid_string):
    dict = {
        'temp': temp_string,
        'humidity': humid_string
    }
    db.child("last").update(dict)


# sends data to Firebase database
def send_data_to_firebase(temp_string, humid_string, light_sensor_value):
    db.child("data").child(time_stamp()).set({
        'fTemp': temp_string,
        'humidity': humid_string,
        'light': light_sensor_value
    })


# sends settings to the Firebase database
def send_settings_to_firebase(too_low_temp, just_right_temp, too_high_temp, humidity_limit, light_threshold):
    db.child("settings").set({
        'too low': too_low_temp,
        'just right': just_right_temp,
        'too hot': too_high_temp,
        'humidity limit': humidity_limit,
        'light threshold': light_threshold
    })


# prints confirmation that data is recorded, and prints the data that was recorded
def print_data_confirmation(temp_string, humid_string):
    print("Temp: " + temp_string + "F\n" + "Humidity: " + humid_string + "%")
    print("This data was recorded!\n")


'''
functions used to read the settings from Firebase
'''


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


'''
functions used to retrieve the most recent temperature and humidity from Firebase database
'''


def get_last_temp():
    temp_from_firebase = str(db.child('last/temp').get().val())
    return temp_from_firebase


def get_last_humidity():
    humidity_from_firebase = str(db.child('last/humidity').get().val())
    return humidity_from_firebase
