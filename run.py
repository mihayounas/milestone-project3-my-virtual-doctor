import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
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

    while True:
        patient_staff = input(
            'Hit "a" to arrange an appointment or "s" for staff login:\n\n'
        )
        patient_staff = patient_staff.lower()

        if patient_staff == 'y':
            staff_login()
            return False

        if patient_staff == 'a':
            arrange_appointment()
            return False

        print('Invalid entry, please try again\n')

     
def   arrange_appointment():
    """
    Will have a function which will allow the patient to arrange his booking
    on a desired date or got back to the main menu
    """
    print("\nWhat will be the best date for an appointment?\n")
    print('Customer data is saved and stored in our data base.')
    agree_booking = input(
        'Please press "Y" to accept or "N" to return and cancel.\n'
    )
    if agree_booking == 'Y':
        # Start appointment process for the user
         get_month(year)
    else:
        get_details_data()


def staff_login():
    """
    If the staff choice was made please log in and you will 
    have two options one is to assep patient and one is to 
    check your own schedule and add days off.
    """
    enter_staff_pass = iamstaff.('PASSWORD')
    staff_welcome = '\nMy Virtual Doctore - Staff ONLY'
    print(staff_welcome.upper())
   