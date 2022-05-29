import gspread
from google.oauth2.service_account import Credentials
import datetime
import re


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
   

def validate_name(name):
    """
    Get input details from the customer.
    Get Full Name and date of birth.
    Displaying the age of the customer.
    """
    fname, lname = name.split(" ")
    for character in name:
        if character.isdigit():
            print("Sorry your name contains a number,please try again...\n")
        else:
            return name
    if fname and lname != 2:
        print(f"Welcome {name}!\n")
    else:
        print("Sorry you must enter minimum 2 names,please try again...\n") 


def get_age():
    day, month, year = born.split('/')
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    age_years = int(convertdays/365)
    print(f"You are {int(age_years)} years old\n.")
    return age_years


def validate_email():
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        print("Valid email...\n")
    else:
        print("Sorry invalid address,please try again...\n")
    
    return email


def validate_symptoms():
    if len(symptoms) < 6:
        print("Please add more details for your doctor.\n")
    else: 
        print("Thank you for your details,a confirmation email will follow.\n")

    return symptoms


def update_worksheet():
    details = SHEET.worksheet("details")
    row = [
        f"{name}", f"{born}", f"{age_years} years", f"{email}", f"{symptoms}"
        ]
    index = 2
    details.insert_row(row, index) 
   
   
welcome_message()
name = input('Please enter your full name with spaces between :\n')
validate_name(name)
born = input("Please enter your date of birth: \n")
age_years = get_age()
email = input("Please enter a valid email address:\n")
validate_email()
symptoms = input("Please enter you symptoms bellow :\n")
validate_symptoms()
update_worksheet()
