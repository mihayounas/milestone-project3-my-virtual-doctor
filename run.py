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
    print('To use this app, hit enter after each choice.\n')
    print('After confirming all your details you will receive\n')
    print('a confirmation email!\n')
    
    name_str = input('Please enter you full name : ')
    name_data = name_str.split(" ")
    while True:
        if name_data == type(name_data):
            return name_data
        else:
           
    validate_data(name_data)

    # birth_str = input("Please enter your date of birth 00/00/0000:\n")
    # print(f"Born On {birth_str}\n")
    # birth_data = birth_str.split("/")
    # validate_data(birth_data)
   

def validate_data(values):
    """
    Inside this function we will check if there will be minimum 2 strings
    to confirm the full name and if the date is in this format 00/00/0000.
    """
    try:
        if len(values) != 2:
            raise ValueError(
                f"Minimum 2 names required you have entered {len(values)}"
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')    


get_details_data()