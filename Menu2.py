# Text menu in Python
from click._compat import raw_input
import Database
import graph


# function which prints menu options to the user
def print_menu_options():
    print(30 * "-", "MENU", 30 * "-")

    print("1. Change Settings")

    print("2. Display Chart and Run System")


# runs the function tro print the menu to the user, and stores their choice in the choice variable
print_menu_options()
choice = input("Enter your choice [1-2]: ")
choice = int(choice)


def menu():
    # the user is asked to enter each of the settings,
    # settings are stored in placeholder variables and sent to the database
    if choice == 1:
        user_too_low_temp = int(input("Enter in Fahrenheit the Temperature deemed too low: "))
        user_just_right_temp = int(input("Enter in Fahrenheit the Temperature deemed just right: "))
        user_too_high_temp = int(input("Enter in Fahrenheit the Temperature deemed too high: "))
        user_humidity_limit = int(input("Enter the humidity limit without the % symbol: "))
        user_light_threshold = int(input("Enter the light threshold value: "))
        Database.send_settings_to_firebase(user_too_low_temp, user_just_right_temp, user_too_high_temp,
                                           user_humidity_limit, user_light_threshold)
        print("Your settings have been configured\n")
        print("The system will now run")

    elif choice == 2:
        # runs the function which displays the graph of temperature and humidity
        print("Here is your Graph!")
        graph.graph()

    else:
        # Any integer inputs other than values 1-2 print an error message
        raw_input("Wrong option selection. Enter any key to try again..")
