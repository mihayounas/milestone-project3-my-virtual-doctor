import gspread
from google.oauth2.service_account import Credentials
import datetime

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
    print('Welcome to My Virtual Doctor !')
    print('\n An app which helps you book your doctor appointments fast!\n')
    print('To use this app, press enter after each choice.\n')
    print('After confirming all your details you will receive\n')
    print('a confirmation email!\n')

    while True:
        admin_or_patient = input(
            'Please press "r" to register an appointment or "a"'
            'for admin area:\n\n'
        )
        if admin_or_patient == 'r':
            confirm_terms()
            get_details_data()
            return False
        print('Invalid entry, please try again\n')


def get_details_data():
    """
    Get input details from the customer.
    Get Full Name and date of birth.
    Displaying the age of the customer.
    """
    name = input('Please enter your full name :\n')
    try:
        name.split()[1]
        print(f"Hello, {name}!")
    except IndexError:
        print("Sorry you will need to enter minimum two names...")

    inputDate = input("Enter the date of birth : ")
    day, month, year = inputDate.split('/')
    isValidDate = True
    try:
        datetime.datetime(int(day), int(month), int(year))
    except ValueError:
        isValidDate = True
    if (isValidDate):
        print("Date of birth is valid ...")
    else:
        print("Date of birth is not valid...")
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    age_years = convertdays/365
    print(f"You are {int(age_years)} years old")


def confirm_terms():
    """
    Function which will let patient decide either to continue 
    with appointment or go back,for example if admin was to log in
    but by mistake pressed "r" or the user doesn't agree to the terms of
    saving of data.
    """
    print('Please note we are saving your details in our database.')
    print('If you agree to the terms plese confirm by pressing')
    book_or_exit = input('"y" or "n" to cancel and go back to the main menu..')

    if book_or_exit == 'y':
        # Start getting details for booking
        print("Thank you please follow the steps to get your appointment : ")
        get_details_data()
    else:
        welcome_message()


welcome_message()
confirm_terms()
get_details_data()