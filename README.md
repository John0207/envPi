# envPi
Hello!

Note: to configure with Firebase project, click on the gear next to "project overview" and select project settings. 
Next scroll down to "Firebase SDK Snippet" and select the config option. Copy the corresponding values into the Database.py file.
  
This project is an environment monitoring system and 
was originally developed using modules from Dexter Industries Raspbian for Robots.

The main purpose of the envPi is to gather data environment over a long-term period, but can be used for any length of time.
A prime example of a use case would be to determine environment conditions over time for a garden location. envPi could
just as well serve as a desktop temperature and humidity display 

envPi consists of a Raspberry Pi model B+ with a Grove Pi+ hat. It gathers temperature, humidity, and brightness or light value data.
envPi outputs temperature and humidity data to an LCD screen, and changes the color of the lcd screen based on 
the data, such as red for if the temperature is "too hot". Settings like what is deemed "too hot" can be set by the user in the menu when the
project is first run.

Temperature, humidity, and light value along with the time of each recording is stored in a Google Firebase database. User settings are also
stored in the database. Defaults are set on each run, so those would need to be reset in the menu each time the project is run.

envPi also has an option in the menu to display a line graph of the temperature and humidity data recorded.

-John Deluccia
