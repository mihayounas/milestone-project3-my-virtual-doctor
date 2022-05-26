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
            return False
        print('Invalid entry, please try again\n')
   

def get_details_data():
    """
    Get input details from the customer.
    Get Full Name and date of birth.
    Displaying the age of the customer.
    """
    name = input('Please enter your full name with spaces between :\n')
    fname, lname = name.split(" ")
    for character in name:
        if character.isdigit():
            print(name)
    else:
        print("Sorry your name contains a number,please try again...")
    return name
    if fname != lname:
        print(f"Welcome {name}!")
    else:
        print("Sorry you must enter minimum 2 names,please try again...")


def validate_date():
    """
    Validating data format for a easy reading and 
    calculating patients age by date of birth
    """
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

    return age

    input("Please enter a valid email: \n")

    return birth_date


def update_worksheet(data, worksheet):
    """
    Receives a list of strings to be inserted into worksheet
    Update the relevant worksheet with the data provided
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} data saved succesfully\n")


welcome_message()
data = get_details_data()
validate_date()