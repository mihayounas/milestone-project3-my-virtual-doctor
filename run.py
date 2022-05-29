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
        return True
        if admin_or_patient == 'a':
            return False
        print('Invalid entry, please try again...\n')
        return True
        admin_login()
# Starting by taking patient's details 


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
    """
    Gets the date of birth input and validates 
    the right date format.
    Calculates age in years .
    """
    day, month, year = born.split('/')
    birth_date = datetime.datetime(int(year), int(month), int(day))
    age = (datetime.datetime.now() - birth_date)
    convertdays = int(age.days)
    age_years = int(convertdays/365)
    print(f"You are {int(age_years)} years old\n.")
    return age_years


def validate_email():
    """
    Validates email addresses by checking 
    for a common pathern and returns a valid email address.
    """
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        print("Valid email...\n")
    else:
        print("Sorry invalid address,please try again...\n")
    
    return email


def validate_symptoms():
    """
    Checks if symptoms message is descriptive enough
    and makes sure that it gives the right information 
    for the appointment.
    """
    if len(symptoms) < 8:
        print("Please add more details for your doctor.\n")
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
        f"{name}", f"{born}", f"{age_years} years", f"{email}", f"{symptoms}"
        ]
    index = 2
    details.insert_row(row, index) 
   

def exit_menu():
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
    exit = input("To manage your appointments press '1' or 'e' to close : \n")
    if exit == "1":
        confirmation_data()
    else:
        print("Thank you for your appoinment!")


def confirmation_data():
    """
    Confirms and return the input data before 
    sending the confirmation email.
    """
    print(f"Name : {name}")
    print(f"DOB : {born}")
    print(f"Age : {age_years} years")
    print(f"Email : {email}")
    print(f"Your message :{symptoms}")
    welcome_message()

# Taking user's Admin details


def admin_login():
    asses_or_shift = input(
        "To asses a patient press 'a' or 's' to manage shift...\n"
    )  
    if asses_or_shift == 'a':
        welcome_message()


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
exit_menu()
exit_screen()
confirmation_data()
