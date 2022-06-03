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
    # Displays a welcome message in blue color Figlet
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
# NAME input
def get_name():
    """
    Gets name input from the user
    """
    # Gets a validated name to display
    name = validate_name()
    if name:
        print(f'Welcome {name}...\n')
    else:
        print("Name not valid,please try again...\n")
    return name


# NAME validation
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
            print(
                "Invalid please try again...\n"
                "First and Last name with space between...\n"
            )
    return True


# Get DATE of birth input
def get_birth_date():
    """
    Getting the date of birth and validting is,
    returning date of birth if it's matching
    the format.
    """
    # Gets a validated date of birth and display it
    date_val = val_date()
    if date_val:
        print(f"Your date of birth is : {date_val}\n")
    else:
        print("Please enter the right format DD/MM/YYY...\n")
    return date_val


# Validate DATE of birth
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
        # Only accept if it contains a /
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


# Get EMAIL input from the user
def get_email():
    """
    Getting the email address and validating the format
    if is matching then return the user email if not
    then restart and getting the email again.
    """
    # Get the email from the user after the validation and display it
    email = validate_email()
    if email:
        print(f"Your email is :{email}")
    else:
        print("Sorry your email is not valid,please try again...\n")
    return email


# Validate EMAIL input
def validate_email():
    """
    Validates email addresses by checking
    for a common pathern and returns a valid email address.
    """
    while True:
        email_val = input("Please enter a valid email address:\n")
        regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
        # Only accept if it's matching the regex format
        if re.search(regex, email_val):
            return email_val
        else:
            print("Sorry your email is not valid,please try again...\n")
    return True


# Get SYMPTOMS input
def get_symptoms():
    """
    Gets the user personalised message describing his
    symptoms for the doctor to know before hand what to
    discuss on their appointment.
    """
    # Get user symptoms and display a response message
    user_symptoms = validate_symptoms()
    if user_symptoms:
        print("Thank you for your details,please chose a date...\n")
    else:
        print("Please add more details for your doctor...\n")
    return user_symptoms


# Validate SYMPTOMS input
def validate_symptoms():
    """
    Checks if symptoms message is descriptive enough
    and makes sure that it gives the right information
    for the appointment.
    """
    while True:
        symptoms_val = input("Please enter you symptoms bellow :\n")
        # Only accept a proper message description
        if len(symptoms_val) > 8:
            return symptoms_val
        else:
            print("Please add more details for your doctor...\n")
    return True


# Update and store the details of the user in the spreadsheet
def update_worksheet():
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    # Get all the details stored into the worksheet
    details = SHEET.worksheet("details")
    row = [
        f"{NAME}", f"{BORN}", f"{EMAIL}",
        f"{SYMPTOMS}", f"{DATE}", f"{TIME}:00"
        ]
    index = 2
    details.insert_row(row, index)


# Pick an appointment date and validate it
def pick_a_date():
    """
    Getting a booking date for the user.
    """
    chosen_date = validate_booking_date()
    if chosen_date:
        print(f"Your {chosen_date} is available...\n")
    else:
        print(f"{chosen_date} is not valid please enter the date again...\n")
    return chosen_date


def validate_booking_date():
    """
    Helps the patient pick a available date and
    displaying a calendar for checking the days.
    """
    while True:
        month_inp = int(
            input("Please enter the month you wish to book for...\n : ")
        )
        year_inp = int(input("Please enter the year...\n "))
        if year_inp >= 2022:
            print(calendar.month(year_inp, month_inp))
        else:
            print("Sorry you have to pick current year 2022 or later...\n")
            return month_inp
        day_inp = input("Enter a day from the calendar...\n")
        date = f"{day_inp}/{month_inp}/{year_inp}"
        if date.__contains__('/'):
            return date
        else:
            print("Sorry your date is invalid,please try again...\n")
    return True


# Gat time for the appoinment
def get_time():
    """
    Gets the time input for the appointment
    and diplays it.
    """
    time_choice = validate_time()
    if time_choice:
        print("Time is valid...\n")
        print("Checking if is available...\n")
        print("Time available...\n")
    else:
        print(
            "Sorry time is invalid please try again,"
            "input only times between 9-18...\n"
        )
    return time_choice


def validate_time():
    """
    Gets time input and validates that
    time is in a timeframe 9 - 18
    """
    while True:
        time_val = input("Please choose a time between 9 - 18...\n")
        if int(time_val) in range(9, 19):
            print("Valid time...\n")
            return time_val
        else:
            print("Time chosen is not available,please try again...\n")
    return True


# exit options
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
    print("Please check your details bellow...\n")
    print(f"Name : {NAME}\n")
    print(f"DOB : {BORN}\n")
    print(f"Email : {EMAIL}\n")
    print(f"Your personalised message to the doctor : {SYMPTOMS}\n")
    print(f"Your appointment date and time : {DATE} at {TIME}:00 ...\n")
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


# Declare global variables used to return all the details
# in confirmation_data function and display it at the end
welcome_message()
NAME = get_name()
BORN = get_birth_date()
EMAIL = get_email()
SYMPTOMS = get_symptoms()
DATE = pick_a_date()
TIME = get_time()
confirmation_data()
update_worksheet()


def main():
    """
    Run all the functions
    """
    welcome_message()
    get_name()
    get_birth_date()
    validate_email()
    get_symptoms()
    pick_a_date()
    get_time()
    confirmation_data()
    update_worksheet()


main()
