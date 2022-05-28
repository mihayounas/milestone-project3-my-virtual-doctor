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
            print("Sorry your name contains a number,please try again...\n")
    else:
        return name
    if fname != lname:
        print(f"Welcome {name}!")
    else:
        print("Sorry you must enter minimum 2 names,please try again...\n") 


def insert_name_data():
    """
    Inserts data into the spreadsheet.
    The top data is new data in spreadsheet.
    """
    name = get_details_data()
    born = input("Enter the date of birth : \n")
    day, month, year = born.split('/')
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    age_years = convertdays/365
    print(f"You are {int(age_years)} years old.")
    details = SHEET.worksheet("details")
    row = [f"{name}", f"{born}", f"{age_years}"]
    index = 2
    details.insert_row(row, index)


def main():
    welcome_message()
    insert_name_data()


main()


