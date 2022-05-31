"""
This module imports date and time
"""
import datetime
import re
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


def welcome_message():
    """
    Welcoming the patients or the admin.
    Giving the choice of booking an appointment
    or logging in as admin.
    """
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
        validate_name()
# Starting by taking patient's details


def validate_name():
    """
    Get input details from the customer.
    Get your Full Name and date of birth.
    Displaying the age of the customer.
    """
    while True:
        names = input('Please enter your full name with spaces between :\n')
        #  Don't accept numbers in name,letters only
        if any(chr.isdigit() for chr in names):
            print(
                "Sorry your Name should contain only letters,"
                "please try again..."
                "\n"
                )
        elif names.__contains__(' '):
            print(f"Welcome {names} !\n")
            return names
        else:
            print("Please enter first and last name...\n")
    return False


def get_age():
    """
    Gets the date of birth input and validates
    the right date format.
    Calculates age in years .
    """
    born_date = input("Please enter your date of birth: \n")
    if born_date.__contains__('/'):
        print(f"Date of birth:{born_date}")
    else:
        print("Sorry please include format 00/00/000...")
        return born_date
    day, month, year = born_date.split('/')
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    user_age = int(convertdays/365)
    print(f"You are {int(user_age)} years old\n")
    return born_date


def validate_email():
    """
    Validates email addresses by checking
    for a common pathern and returns a valid email address.
    """
    email_val = input("Please enter a valid email address:\n")
    regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
    if re.search(regex, email_val):
        print(f"Valid Email : {email_val}")
    else:
        print("Sorry your email is not valid,please try again...\n")
    return email_val


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
        pick_a_date()

    return symptoms_val


def update_worksheet():
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    details = SHEET.worksheet("details")
    row = [
        f"{NAME}", f"{BORN}", f"{EMAIL}",
        f"{SYMPTOMS}"
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
    # print(f"Your appointment is on {date} at {chosen_time}")
    change_app = input(
        "If you wish to make any changes press '1' or 'e' to exit...\n"
        )
    if change_app == '1':
        print("Thank you for your booking!\n")
        return False
    else:
        print("Thank you...")
        main()
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
    dates = [
        'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
        'oct', 'nov', 'dec'
        ]
    date_chosen = input(
        "Please enter the first 3 letters of the month...\n"
        "...\n"
    )
    if any(item in date_chosen for item in dates):
        print(f"Month chosen is {date_chosen}")
    else:
        print("Please check the format required...\n")
    return date_chosen


def get_time():
    """
    Gets time input and validates that
    time is in a timeframe 9 - 18
    """
    time_val = input("Please choose a time between 9 - 18...\n")
    time_choice = range(9, 19)
    if time_val in time_choice:
        print("Time available...\n")
    else:
        print("Time chosen is not available,please try again...\n")
    return time_val


# Declare global variables used to return all the details
welcome_message()
NAME = validate_name()
BORN = get_age()
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
    validate_name()
    get_age()
    validate_email()
    validate_symptoms()
    pick_a_date()
    get_time()
    update_worksheet()
    confirmation_data()


main()
