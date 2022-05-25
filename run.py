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


def get_details_data():
    """
    Get input details from the customer .
    """

    print('Welcome to My Virtual Doctor !')
    print('\n An app which helps you book your doctor appointments fast!\n')
    print('To use this app, press enter after each choice.\n')
    print('After confirming all your details you will receive\n')
    print('a confirmation email!\n')
    name = input('Please enter your full name :')
    try:
        name.split()[1]
        print(f"Hello, {name}!")
    except IndexError:
        print("Sorry you will need to enter minimum two names...")

    # birth_str = input("Please enter your date of birth 00/00/0000:\n")
    # print(f"Born On {birth_str}\n")
    # birth_data = birth_str.split("/")
    # validate_data(birth_data)

    
get_details_data()