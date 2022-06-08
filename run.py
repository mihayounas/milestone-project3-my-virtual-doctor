"""
Main My Virtual Doctor file for a command line interface appointments
system for patients and admins.

This app's purpose is to help patients to book their appointments
change or cancel it.

The information of the user is saved into a spreadsheet on Google drive.
"""
import datetime
import re
import calendar
# import Pyfiglet library for text to fonts functionality
from pyfiglet import Figlet
# import Termcolor library for text colours
from termcolor import colored
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


def welcome_msg(text):
    """
    Welcome message with special figlet styling.
    """
    # Displays a welcome message in cyan color Figlet
    font = Figlet(font="slant")
    print(colored(font.renderText(text), "cyan",  attrs=["bold"]))


def welcome_message():
    """
    Welcoming the patients or the admin.
    Giving the choice of booking an appointment
    or logging in as admin.
    """
    welcome_msg("My Virtual Doctor...")
    print("-" * 80)
    print("-" * 80)
    print('Welcome to My Virtual Doctor !')
    print('An app which helps you book your doctor appointments fast!')
    print('To use this app, press enter after each choice.')
    print('After confirming all your details you will be able')
    print('to see, edit or cancel your appoinment...!')
    while True:
        admin_or_patient = input(
            'Please press "r" to register an appointment or "a" '
            'for admin area:\n'
        )
        if admin_or_patient == 'r':
            return False
        if admin_or_patient == 'a':
            asses_patient_or_shift()
            main_admin()
            return False
        print(colored('Invalid entry, please try again...\n', 'red'))
    return True


# Starting by taking patient's details
# NAME input
def get_name():
    """
    Gets name input from the user
    """
    # Gets a validated name to display
    print("-" * 80)
    name = validate_name()
    if name:
        print(f'Welcome {name}...\n')
    else:
        print("Name not valid,please try again...")
    print("-" * 80)
    return name


# NAME validation
def validate_name():
    """
    Get input details from the customer.
    Get your Full Name and date of birth.
    Displaying the age of the customer.
    """
    while True:
        names = input("Please enter your full name with space between...\n")
        if len(names) <= 2:
            print(
                colored(
                    "Please enter your full name with space between...\n",
                    'red'
                    )
                    )

        #  Don't accept numbers in name
        elif any(char.isdigit() for char in names):
            print("Names should not contain numbers...")

        #  Only accept the names if contains a space
        elif names.__contains__(' '):
            return names


# Get DATE of birth input
def get_birth_date():
    """
    Getting the date of birth and validating is,
    returning date of birth if it's matching
    the format.
    """
    print("-" * 80)
    # Gets a validated date of birth and display it
    date_val = val_date()
    if date_val:
        print(f"Your date of birth is : {date_val}\n")
        day, month, year = date_val.split('/')
        birth_date = datetime.datetime(int(year), int(month), int(day))
        age_years = (datetime.datetime.now() - birth_date)
        convertdays = int(age_years.days)
        age_years = int(convertdays/365)
        print(f"Your are {age_years} years old...\n")
        return date_val
    else:
        print(colored("Please enter the right format DD/MM/YYY...\n", 'red'))
        return date_val


# Validate DATE of birth
def val_date():
    """
    Validates and calculates age of the user
    by the date of birth.
    """
    while True:
        date_input = input(
            "Please enter your date of birth in this "
            "format DD/MM/YYYY:\n"
        )
        format_str = "%d/%m/%Y"
        try:
            datetime.datetime.strptime(date_input, format_str)
            return date_input
        except ValueError:
            print(
                colored(
                    "This format is incorrect,it should be DD/MM/YYY/...",
                    'red')
                    )
    return True


# Get EMAIL input from the user
def get_email():
    """
    Getting the email address and validating the format
    if is matching then return the user email if not
    then restart and getting the email again.
    """
    print("-" * 80)
    # Get the email from the user after the validation and display it
    email = validate_email()
    if email:
        print(f"Your email is :{email}\n.")
    else:
        print(
            colored(
                "Sorry your email is not valid,please try again...\n", 'red'
            )
            )
    return email


# Validate EMAIL input
def validate_email():
    """
    Validates email addresses by checking
    for a common pathern and returns a valid email address.
    """
    while True:
        email_val = input("Please enter a valid email address:\n")
        regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
        # Only accept if it's matching the regex format
        if re.search(regex, email_val):
            return email_val
        else:
            print(
                colored(
                    "Sorry your email is not valid,please try again...\n",
                    'red'
                    )
                    )
    return True


# Get SYMPTOMS input
def get_symptoms():
    """
    Gets the user personalised message describing his
    symptoms for the doctor to know before hand what to
    discuss on their appointment.
    """
    print("-" * 80)
    # Get user symptoms and display a response message
    user_symptoms = validate_symptoms()
    if user_symptoms:
        print("Thank you for your details,please chose a date...\n")
    else:
        print(
            colored(
                "Please add more details for your doctor...\n", 'red'
                )
                )
    return user_symptoms


# Validate SYMPTOMS input
def validate_symptoms():
    """
    Checks if symptoms message is descriptive enough
    and makes sure that it gives the right information
    for the appointment.
    """
    while True:
        symptoms_val = input("Please enter you symptoms bellow :\n")
        # Only accept a proper message description
        if len(symptoms_val) > 8:
            return symptoms_val
        else:
            print(
                colored(
                    "Please add more details for your doctor...\n", 'red'
                    )
                    )
    return True


# Pick an appointment date and validate it
def pick_a_date():
    """
    Getting a booking date for the user.
    """
    print("-" * 80)
    chosen_date = validate_booking_date()
    if chosen_date:
        print(f"Your {chosen_date} is available...\n")
    else:
        print(f"{chosen_date} is not valid please enter the date again...\n")
    return chosen_date


def validate_booking_date():
    """
    Helps the patient pick a available date and
    displaying a calendar for checking the days.
    """
    while True:
        mydate = datetime.datetime.now()
        mydate.strftime("%b")
        print(colored(f"Today's date is {mydate}", 'yellow'))
        print("Please enter a date further in time to validate...")
        year_inp = int(input("Please enter the year...\n "))
        month_inp = int(
            input("Please enter the month you wish to book for 1-12...\n : ")
        )
        if year_inp >= 2022:
            print(calendar.month(year_inp, month_inp))
        else:
            print("Sorry you have to pick current year 2022 or later...\n")
            return year_inp
        if "month_inp" >= mydate.strftime("%b"):
            print("Date not available,please try again...")
            return month_inp
        if month_inp <= 12:
            print("Month input is valid...")
        else:
            print("Not valid...")
            return month_inp
        day_inp = input("Enter a day from the calendar...\n")
        date = f"{day_inp}/{month_inp}/{year_inp}"
        if date.__contains__('/'):
            return date
        else:
            print(
                colored(
                    "Sorry your date is invalid,please try again...\n", 'red'
                )
                )
            return month_inp
    return True


# Gat time for the appoinment
def get_time():
    """
    Gets the time input for the appointment
    and diplays it.
    """
    print("-" * 80)
    time_choice = validate_time()
    if time_choice:
        print("Time is valid...\n")
        print("Checking if is available...\n")
        print("Time available...\n")
    else:
        print(
            colored(
                "Sorry time is invalid please try again,"
                "input only times between 9-18...\n"
                )
                )
    return time_choice


def validate_time():
    """
    Gets time input and validates that
    time is in a timeframe 9 - 18
    """
    while True:
        time_val = input("Please enter a time between 9 - 18...\n")
        if int(time_val) in range(9, 19):
            print("Valid time...\n")
            return f"{time_val}:00"
        else:
            print(
                colored(
                    "Time chosen is not available,please try again...\n", 'red'
                    )
                    )
    return True


# Taking user's Admin details
def val_admin_message():
    """
    Gets a message from the admin like a holiday
    request of shift change
    """
    while True:
        message = input(
            "Please enter your request bellow, to be checked and approved"
            " by manager on shift make sure to include the dates you are "
            "are requesting for...\n"
            )
        print(
            f"Your message: [{message}] will be checked and manager"
            " will approve it shortly...\n"
            )
        if len(message) > 8:
            return message
        else:
            print(
                colored(
                    "Please add more details to describe the situation"
                    "for the manager...\n", 'pink'
                    )
                    )
    return True


def admin_shift_management():
    """
    Takes admin requests and store it into the spreadsheet
    for the managers to check and approve.
    """
    # Takes admin name and validates it and then takes patient details
    admin_name = input("Please enter your full name : \n")
    if len(admin_name) > 4:
        print(
            f"Welcome {admin_name}, please follow the next steps in"
            "order to send your request..."
        )
    else:
        print("Name not valid,please try again...\n")
        print("-" * 0)
    return admin_name


def asses_patient_or_shift():
    """
    Gets the choice from the admin if he wants to asses patient
    or manage the shift and holidays requests.
    """
    print("-" * 80)
    admin_val = admin_login()
    asses_or_shift = input(
            "To asses a patient press 'a' or 's' to manage shift...\n"
        )
    if admin_val:
        return admin_val
    else:
        print("Logged in ...\n")
    if asses_or_shift == 'a':
        print(
            "Please assess your patients carefully...\n"
            )
        main_user()
        # Asses patients over the phone or over the counter
        # and enter their details
    if asses_or_shift == 's':
        admin_shift_management()


def admin_login():
    """
    This function will enter the admin only area
    and will have a choice of asses the patient
    or open the screen to manage the weekly shift.
    """
    print("-" * 80)
    admin_pass = 'Admin'
    inputs = 0
    admin_welcome = 'Welcome Admin'
    welcome_msg(admin_welcome)
    while True:
        admin_pass_input = input(
            "Please enter your password to log in...\n"
            )
        if inputs == 3:
            print(
                "You have reached maximum attempts, password is invalid..."
                "Please start again...\n"
                )
            welcome_message()
            return False
        if admin_pass_input == admin_pass:
            print("Valid Password...\n")
            return False
        else:
            print('\nWrong password, please try again\n')
            inputs += 1
    return True


def get_shift_days():
    """
    Gets information about each admin's personal shift
    in order to get the infor into the spreadsheet
    for the manager to analyse and approve.
    """
    shift_info = input(
        "Please enter the days of the week that you work,"
        "separated by comma...\n"
        )
    if shift_info.__contains__(','):
        return shift_info
    else:
        print("Please separate the days by comma...\n")
    return shift_info


def get_shift_times():
    """
    Gets shift times from the admin and store it into the
    spreadsheet for manager to assess...
    """
    shift_time = input("Please enter the shift times...\n")
    if shift_time:
        print("Thank you for your details...\n")
        print("We can confirm that your data is correct...\n")
    else:
        print(
            "Sorry this data does not match our records, please try again...\n"
            )
    return shift_time


# exit options
def exit_menu():
    """
    The exit menu will offer a choice to user,
    he can return to the main menu and start
    again or can exit the screen.
    """
    print("-" * 80)
    menu_exit = input(
        colored(
            "Please press 'm' for main menu or 'e' to exit...\n", 'blue'
            )
            )
    if menu_exit == "m":
        main_user()
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
    print("-" * 0)
    print("Thank you for visiting our application !\n")
    print("What would you like to do next ?\n")
    exit_choice = input(
        "To manage your appointments press '1' or 'e' to close:\n"
        )
    if exit_choice == "1":
        collect_data()
    else:
        text = "GoodBye...\n"
        welcome_msg(text)


# Update and store the details of the user in the spreadsheet
def update_worksheet(data, worksheet):
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    # Get all the details stored into the worksheet
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print("Thank you,your details have been succesfully saved...\n")


def cancel_or_change_data():
    """
    Gets the answer from user of the action
    that he wants to take.
    """
    cancel_or_change = input(
        "If you would like to cancel or change your appoinment "
        "press '1' or 'e' to exit"
        )
    if cancel_or_change == 1:
        collect_data()
    else:
        exit_screen()
    return cancel_or_change


def collect_data():
    """
    Displays data for the user in order to allow them
    to cancel or change their appoinment
    """
    email = get_email()
    worksheet = SHEET.worksheet('details')
    emails = worksheet.col_values(3)
    regex1 = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$"
    for email in emails:
        if re.fullmatch(regex1, email):
            return f"{email} is matching our records..."
        else:
            print("No email matching...")
            return email
    name_details = worksheet.col_values(1)
    print(name_details)
    date_of_birth_details = worksheet.col_values(2)
    print(date_of_birth_details)
    symptoms_details = worksheet.col_values(4)
    print(symptoms_details)
    app_date = worksheet.col_values(5)
    print(app_date)
    app_time = worksheet.col_values(6)
    print(app_time)


def main_user():
    """
    Run all the functions for user input, validation
    and saving into the spreadsheet...
    """
    name_user = get_name()
    birth_date = get_birth_date()
    email_user = validate_email()
    symptoms_user = get_symptoms()
    date_user = pick_a_date()
    time_user = get_time()
    data = [
        name_user, birth_date, email_user, symptoms_user, date_user,
        time_user
        ]
    update_worksheet(data, 'details')
    exit_screen()
    values_data = cancel_or_change_data()
    return values_data


def main_admin():
    """
    Run all the functions for admin section when called
    """
    # Get all the details stored into the worksheet
    admin_input_name = admin_shift_management()
    shift_days = get_shift_days()
    shift_times = get_shift_times()
    admin_mess = val_admin_message()
    data = [admin_input_name, shift_days, shift_times, admin_mess]
    update_worksheet(data, "admin")
    exit_menu()


welcome_message()
main_user()
