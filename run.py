import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "http://www.googleapis.com/auth/calendar"
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
    print('To use this app, hit enter after each choice.\n')
    print('After confirming all your details you will receive\n')
    print('a confirmation email!\n')
    
    data_str = input("Please Enter Your Full Name here:\n")
    print(f"Hello {data_str}\n")


get_details_data()