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
    name = input('Please enter your full name with spaces between :\n')
    fname, lname = name.split(" ")
    if len(fname) < 2:
        print("Sorry you must enter your first name, please try again...\n")
        validate_name()
    if len(lname) < 2:
        print("Sorry you must enter your last name, please try again...\n")
        validate_name()
    if any(chr.isdigit() for chr in name):
        print(
            "Sorry your Name should contain only letters,please try again..."
            "\n"
        )
        validate_name()
        return False
    else:
        print(f"Welcome {name} !\n")
    return name


def get_age():
    """
    Gets the date of birth input and validates
    the right date format.
    Calculates age in years .
    """
    day, month, year = born.split('/')
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    user_age = int(convertdays/365)
    print(f"You are {int(user_age)} years old\n")
    return user_age


def validate_email():
    """
    Validates email addresses by checking
    for a common pathern and returns a valid email address.
    """
    email = input("Please enter a valid email address:\n")
    regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
    if re.search(regex, email):
        print(f"Valid Email : {email}")
    else:
        print("Sorry your email is not valid,please try again...\n")
        validate_email()
        return True
    return email


def validate_symptoms():
    """
    Checks if symptoms message is descriptive enough
    and makes sure that it gives the right information
    for the appointment.
    """
    symptoms = input("Please enter you symptoms bellow :\n")
    if len(symptoms) < 5:
        print("Please add more details for your doctor.\n")
        validate_symptoms()
    else:
        print("Thank you for your details,a confirmation email will follow.\n")

    return symptoms


def update_worksheet():
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    details = SHEET.worksheet("details")
    row = [
        f"{val_name}", f"{born}", f"{age_years} years", f"{email_val}",
        f"{symptoms_val}"
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
        welcome_message()
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
    print("Thank you for visiting our application !")
    print("What would you like to do next ?")
    exit_choice = input(
        "To manage your appointments press '1' or 'e' to close:\n"
        )
    if exit_choice == "1":
        return False
    print("Thank you for your appoinment!")
    welcome_message()


def confirmation_data():
    """
    Confirms and return the input data before
    sending the confirmation email.
    """
    print(f"Name : {val_name}")
    print(f"DOB : {born}")
    print(f"Age : {age_years} years")
    print(f"Email : {email_val}")
    print(f"Your message :{symptoms_val}")
    change_app = input(
        "If you wish to make any changes press '1' or 'e' to exit...\n"
        )
    if change_app == '1':
        return False
    print("Thank you for your booking!\n")
    welcome_message()
    validate_name()
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
    date_chosen = input(
        "Please enter day and first three letters of the month...\n"
    )


welcome_message()
val_name = validate_name()
born = input("Please enter your date of birth: \n")
age_years = get_age()
email_val = validate_email()
symptoms_val = validate_symptoms()
update_worksheet()
confirmation_data()
