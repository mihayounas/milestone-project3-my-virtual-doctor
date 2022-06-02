"""
This module imports date and time
"""
import datetime
import re
import calendar
# import Pyfiglet library for text to fonts functionality
from pyfiglet import Figlet
# import Termcolor library for text colours
from termcolor import colored
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("my_virtual_doctor")


def welcome_msg(text):
    """
    Print banner msg using Figlet font.
    """
    font = Figlet(font="ogre")
    print("-" * 120)
    print(colored(font.renderText(text), "blue"))
    print("-" * 120)


def welcome_message():
    """
    Welcoming the patients or the admin.
    Giving the choice of booking an appointment
    or logging in as admin.
    """
    text = "Welcome"
    welcome_msg(text)
    print('Welcome to My Virtual Doctor !\n')
    print('An app which helps you book your doctor appointments fast!\n')
    print('To use this app, press enter after each choice.\n')
    print('After confirming all your details you will receive\n')
    print('a confirmation email!\n')
    while True:
        admin_or_patient = input(
            'Please press "r" to register an appointment or "a"'
            'for admin area:\n'
        )
        if admin_or_patient == 'r':
            return False
        print('Invalid entry, please try again...\n')
    return True
# Starting by taking patient's details


def get_name():
    """
    Gets name input from the user
    """
    name = validate_name()
    if name:
        print(f'Welcome {name}...\n')
    else:
        print("Name not valid,please try again...\n")
    return name


def validate_name():
    """
    Get input details from the customer.
    Get your Full Name and date of birth.
    Displaying the age of the customer.
    """
    while True:
        names = input('Please enter your first and last name with space:\n')
        #  Don't accept numbers in name,letters only
        if any(chr.isdigit() for chr in names):
            print(
                "Sorry your Name should contain only letters,"
                "please try again..."
                "\n"
                )
            return False
        #  Only accept if name contains a space
        elif names.__contains__(' '):
            return names
        else:
            print("Please enter your first and last name...\n")
    return True


def get_birth_date():
    date_val = val_date()
    if date_val:
        print(f"Your date of birth is : {date_val}\n")
    else:
        print("Please enter the right format DD/MM/YYY...\n")
    return date_val


def val_date():
    """
    Validates and calculates age of the user
    by the date of birth.
    """
    while True:
        date_input = input(
            "Please enter your date of birth in this "
            "format DD/MM/YYYY:\n"
        )
        if date_input.__contains__("/"):
            format_str = "%d/%m/%Y"
            datetime.datetime.strptime(date_input, format_str)
            return date_input
        else:
            print(
                "This is the incorrect date format.It should be "
                "DD/MM/YYYY...\n"
                )
    return True


def validate_email():
    """
    Validates email addresses by checking
    for a common pathern and returns a valid email address.
    """
    while True:
        email_val = input("Please enter a valid email address:\n")
        regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
        if re.search(regex, email_val):
            print(f"Valid Email : {email_val}")
            return False
        else:
            print("Sorry your email is not valid,please try again...\n")
    return True


def validate_symptoms():
    """
    Checks if symptoms message is descriptive enough
    and makes sure that it gives the right information
    for the appointment.
    """
    symptoms_val = input("Please enter you symptoms bellow :\n")
    if len(symptoms_val) < 5:
        print("Please add more details for your doctor.\n")
        validate_symptoms()
    else:
        print("Thank you for your details,please chose a date...\n")

    return symptoms_val


def update_worksheet():
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    details = SHEET.worksheet("details")
    row = [
        f"{NAME}", f"{BORN}", f"{EMAIL}",
        f"{SYMPTOMS}", f"{DATE}", f"{TIME}:00"
        ]
    index = 2
    details.insert_row(row, index)


def exit_menu():
    """
    The exit menu will offer a choice to user,
    he can return to the main menu and start
    again or can exit the screen.
    """
    menu_exit = input("Please press 'm' for main menu or 'e' to exit...\n")
    if menu_exit == "m":
        main()
    else:
        exit_screen()


def exit_screen():
    """
    This is an exit function wich gives the opportunity
    for the patient to see his appointment and manage it ,
    cancel it or reschedule it.
    Also there is an option to close it and take them to
    the main screen.
    """
    print("Thank you for visiting our application !\n")
    print("What would you like to do next ?\n")
    exit_choice = input(
        "To manage your appointments press '1' or 'e' to close:\n"
        )
    if exit_choice == "1":
        return False
    print("Thank you for your appoinment!\n")
    main()


def confirmation_data():
    """
    Confirms and return the input data before
    sending the confirmation email.
    """
    print(f"Name : {NAME}")
    print(f"DOB : {BORN}")
    print(f"Email : {EMAIL}")
    print(f"Your message :{SYMPTOMS}")
    print(f"Your appointment is on {DATE} at {TIME}:00 ")
    # print(f"Your appointment is on {date} at {chosen_time}")
    change_app = input(
        "If you wish to make any changes press '1' or 'e' to exit...\n"
        )
    if change_app == '1':
        print("Thank you for your booking!\n")
        return False
    else:
        text = "Thank you..."
        welcome_msg(text)
# Taking user's Admin details


def admin_login():
    """
    This function will enter the admin only area
    and will have a choice of asses the patient
    or open the screen to manage the weekly shift.
    """
    asses_or_shift = input(
        "To asses a patient press 'a' or 's' to manage shift...\n"
    )
    if asses_or_shift == 'a':
        welcome_message()


def pick_a_date():
    """
    Helps the patient pick a available date and time
    """
    month_inp = int(
        input("Please enter the month you wish to book for...\n : ")
        )
    year_inp = int(input("Please enter the year...\n "))
    print(calendar.month(year_inp, month_inp))
    day_inp = input("Enter a day from the calendar...\n")
    print(f"Your booking date is {day_inp}/{month_inp}/{year_inp}...\n")
    pick_choice = input("Please press '1' to confirm or 'e' to exit")
    if pick_choice == '1':
        confirmation_data()
    else:
        exit_screen()
    return (f"{day_inp}/{month_inp}/{year_inp}")


def get_time():
    """
    Gets time input and validates that
    time is in a timeframe 9 - 18
    """
    time_val = input("Please choose a time between 9 - 18...\n")
    if int(time_val) in range(9, 19):
        print("Time chosen is not available,please try again...\n")
        return time_val
    else:
        print("Valid time...\n")
    return time_val


# Declare global variables used to return all the details
welcome_message()
NAME = get_name()
BORN = get_birth_date()
EMAIL = validate_email()
SYMPTOMS = validate_symptoms()
DATE = pick_a_date()
TIME = get_time()
update_worksheet()
confirmation_data()


def main():
    """
    Run all the functions
    """
    welcome_message()
    get_name()
    get_birth_date()
    validate_email()
    validate_symptoms()
    pick_a_date()
    get_time()
    update_worksheet()
    confirmation_data()


main()
