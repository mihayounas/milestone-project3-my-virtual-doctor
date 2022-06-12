"""
Main My Virtual Doctor file for a command line interface it is
an appointment system for patients and admins.

This app's purpose is to help patients to book their appointments,
change or cancel it.

The information of the user is saved into a spreadsheet on Google drive.

It also gives the option for the admins to assess the patients or send a
holiday request which is also stored into the spreadsheet.
"""
# Datetime import to handle date and time
import datetime
import re
import time
# Pyfiglet library for text to fonts functionality
from pyfiglet import Figlet
# Termcolor library for text colours
from termcolor import colored
# Google spreadsheets to save our data
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


# Welcome function which will help display welcome message
def welcome_msg(text):
    """
    Welcome message with special figlet styling.
    """
    # Displays a welcome message in cyan color Figlet
    font = Figlet(font="cybermedium")
    print(colored(font.renderText(text), "cyan",  attrs=["bold"]))


# Welcome message with description of the application
def welcome_message():
    """
    Welcoming the patients or the admin.
    Giving the choice of booking an appointment
    or logging in as admin.
    """
    welcome_msg("My Virtual Doctor")
    print("-" * 80)
    print("-" * 80)
    print('Welcome to My Virtual Doctor app...!')
    print('An app which helps you book your doctor appointments fast!')
    print('To use this app, press enter after each choice.')
    print('After confirming all your details you will be able')
    print('to see, edit or cancel your appoinment...!\n')

    print(
        "After each information entered please press enter to send your"
        " response.\n"
        )
    while True:
        # Gives the option for patient or admin user
        admin_or_patient = input(
            'Please press "r" to register an appointment or "a" '
            'for admin area or '
            'if you have an appoinment press "1":\n'
        )
        # This part will start taking patient's details
        if admin_or_patient == 'r':
            return False
        # This part will start taking admins's details
        if admin_or_patient == 'a':
            asses_patient_or_shift()
            main_admin()
            return False
        # This part will help someone already registered
        # to manage his appoinment
        if admin_or_patient == '1':
            collect_data()
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
    print(
        "PLease note that your details will be saved into our database..."
        )
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
            day, month, year = date_input.split('/')
            birth_date = datetime.datetime(int(year), int(month), int(day))
            # Calculates age in years for the patient
            age_years = (datetime.datetime.now() - birth_date)
            convertdays = int(age_years.days)
            age_years = int(convertdays/365)
            # It won't take anything later than 110 years old
            if age_years < 110:
                print("valid")
                print(f"Your are {age_years} years old...\n")
            else:
                print('The year you entered is invalid,please try again...\n')
                continue
        except ValueError:
            print(
                colored(
                    "This format is incorrect,it should be DD/MM/YYY/...",
                    'red')
                    )
            continue
        return date_input
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
        if len(symptoms_val) > 7:
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
    date_choice = validate_booking_date()
    if date_choice:
        print(f'Date {date_choice} is available...\n')
    else:
        print("Not valid,please try again...")
    print("-" * 80)
    return date_choice


# Validates a date in future ,do not accept past dates
def validate_booking_date():
    """
    Helps the patient pick a available date and
    displaying a calendar for checking the days.
    """
    while True:
        date_user_input = input(
            "Please enter your the appoinment date DD/MM/YYYY:\n"
            )
        format_str = "%d/%m/%Y"
        today_date = (time.strftime("%d/%m/%Y"))
        print(colored("This is today's date: " + today_date, 'yellow'))

        if date_user_input > today_date:
            print("Valid date...saving...")
            return date_user_input
        else:
            print(colored("Invalid,please try again...", 'red'))
            continue
        try:
            datetime.datetime.strptime(date_user_input, format_str)
            return date_user_input
        except ValueError:
            print(
                colored(
                    "This format is incorrect,it should be DD/MM/YYY/...",
                    'red')
                    )
    return True


# Get time for the appoinment
def get_time():
    """
    Gets the time input for the appointment
    and diplays it.
    """
    print("-" * 80)
    time_choice = validate_time()
    if time_choice:
        print(f"{time_choice}:00 is available...\n")
    else:
        print(
            colored(
                "Sorry time is invalid please try again,"
                "input only times between 9-18...\n"
                )
                )
    return time_choice


# Validates the time input
def validate_time():
    """
    Gets time input and validates that
    time is in a timeframe 9 - 18
    """
    while True:
        time_val = input("Please enter a time between 9 - 18...\n")
        try:
            if int(time_val) in range(9, 19):
                print("Time is valid...saving...")
                return f"{time_val}"
            else:
                print(
                    colored(
                        "This is not valid...please try again...",
                        'red')
                        )
                continue
        except ValueError:
            print(
                colored(
                    "This is not valid...please try again...",
                    'red')
                    )
    return True


# Taking user's Admin details
def asses_patient_or_shift():
    """
    Gets the choice from the admin if he wants to asses patient
    or manage the shift and holidays requests.
    """
    print("-" * 80)
    while True:
        admin_val = admin_login()
        if admin_val:
            return admin_val
        else:
            print("Logged in ...\n")
        asses_or_shift = input(
                "To assess a patient press 'a' or 's' to manage shift...\n"
            )
        if asses_or_shift == 'a':
            print(
                "Please assess your patients carefully...\n"
                )
            main_user()
            # Asses patients over the phone or over the counter
            # and enter their details
        if asses_or_shift == 's':
            # Will take Admin's details
            print("Please enter your details...")
            admin_shift_management()
    return True


# Admin log in area
def admin_login():
    """
    This function will enter the admin only area
    and will have a choice of asses the patient
    or open the screen to manage the weekly shift.
    """
    print("-" * 80)
    # Admin password - I will hide in the future but use it like this for
    # this project
    admin_pass = 'Admin'
    inputs = 0
    admin_welcome = 'Welcome Admin'
    welcome_msg(admin_welcome)
    while True:
        admin_pass_input = input(
            "Please enter your password to log in...\n"
            )
        # If wrong password too many time it will go to Admin Welcome page
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
            print(colored('\nWrong password, please try again\n', 'red'))
            inputs += 1
    return True


# Entering details for admin and getting their message to be stored
def admin_shift_management():
    """
    Takes admin requests and store it into the spreadsheet
    for the managers to check and approve.
    """
    while True:
        # Takes admin name and validates it and then takes patient details
        admin_name = validate_name()
        if admin_name:
            print(
                f"Welcome {admin_name}, please follow the next steps in "
                "order to send your request..."
            )
        else:
            print("Name not valid,please try again...\n")
            print("-" * 0)
            return admin_name
        get_shift_days()
        get_shift_times()
        val_admin_message()
    return True


# Getting admin shift days
def get_shift_days():
    """
     Gets information about each admin's personal shift
    in order to get the info into the spreadsheet
    for the manager to analyze and approve.
    """
    shift_days = val_days()
    if shift_days:
        print(f"Days you work:{shift_days}")
    else:
        print("Please enter correct values...\n")
    return shift_days


# Validates shift days for admin
def val_days():
    """
    Validates the shift days input, days with comma
    between.
    """
    while True:
        shift_info = input(
            "Please enter the days of the week that you work,"
            "separated by comma...\n"
            )
        try:
            if shift_info.__contains__(','):
                return shift_info
            else:
                print(
                    colored(
                        "This is not valid...please try again...",
                        'red')
                        )
                continue
        except ValueError:
            print(
                colored(
                    "This is not valid...please try again...",
                    'red')
                    )
    return True


# Gets admin's working times
def get_shift_times():
    """
    Gets shift times from the admin and store it into the
    spreadsheet for manager to assess...
    """
    while True:
        print("Please enter the shift times...\n")
        shift_time = validate_time()
        if shift_time:
            print("Thank you for your details...\n")
            print("We can confirm that your data is correct...\n")
        else:
            print("Invalid,data does not match our records...\n")
        return shift_time
    return True


# Gets admin's personalised message for a holiday request
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
        try:
            # Input message has to be clear and descriptive
            if len(message) > 8:
                print(
                    f"Your message: [{message}] will be checked and manager"
                    " will approve it shortly...\n"
                    )
                return message
            else:
                print(
                    "Sorry this data does not match our records, "
                    "please try again...\n"
                    )
                continue
        except ValueError:
            print("Invalid,try again...")
    return True


# Gives option to on to the main menu or exit screen
def exit_menu():
    """
    The exit menu will offer a choice to user,
    he can return to the main menu and start
    again or can exit the screen.
    """
    print("-" * 80)
    while True:
        menu_exit = input(
            colored(
                "Please press 'c' to continue or 'e' to exit...\n", 'blue'
                )
                )
        if menu_exit != "c":
            exit_screen()
        else:
            main_user()
    return True


# Gives option to see the existing appoinment details or close the app
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
    while True:
        exit_choice = input(
            "To manage your appointments press '1' or 'e' to close:\n"
            )
        if exit_choice == "1":
            collect_data()
        else:
            text = "GoodBye...\n"
            welcome_msg(text)
            break
    return True


# Update and store the details of the user in the spreadsheet
def update_worksheet(data, worksheet):
    """
    Updates the right worksheet in order
    to store patient details into the database.
    """
    # Get all the details stored into the worksheet
    new_data_worksheet = SHEET.worksheet(worksheet)
    new_data_worksheet.append_row(data)
    print("Thank you,your details have been succesfully saved...\n")


# Offers option to cancel or change the appoinment
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


# Collect the data already save into the spreadsheet
def collect_data():
    """
    Displays data for the user in order to allow them
    to cancel or change their appoinment
    """
    worksheet = SHEET.worksheet('details')
    emails = worksheet.col_values(3)
    email = validate_email()
    regex1 = re.compile("^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+.[a-z]{1,3}$")
    # Matching the email to the regex to validate it is an email
    # Finds where the email is,if it exists it's matching it
    if re.fullmatch(regex1, email):
        if email in emails:
            print("Your email is matching our records...\n")
        else:
            print("Sorry you are not registered yet...\n")
            exit_menu()
    print("Your appoinment details:")
    # Collects the name matching to the email
    name_row = worksheet.find(email).row
    name = worksheet.cell(name_row, 1).value
    print(f"Name: {name}")
    # Collects the date matching to the email
    date_row = worksheet.find(email).row
    app_date = worksheet.cell(date_row, 5).value
    print(f"Date: {app_date}")
    # Collects the appoinment time matching to the email
    time_row = worksheet.find(email).row
    app_timming = worksheet.cell(time_row, 6).value
    print(f"Time: {app_timming}:00")
    print("Please enter your new details...")
    # Collects new details for a new appoinment
    name_new = get_name()
    date_new = pick_a_date()
    time_new = get_time()
    new_data = [name_new, date_new, time_new]
    update_worksheet(new_data, 'rescheduled')


# Removes the old appoinment and keeps the new one
def cancel_appoinment():
    """
    Cancel app
    """
    cancel_input = input(
        "Please press '1' to change the date or 'c' to cancel your appoinment"
        "...\n"
        )
    if cancel_input == '1':
        validate_booking_date()
        get_time()
        print("Your appointment has been changed...")
        exit_screen()
    else:
        print("deleted...")


# Main User App functions
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


# Main Admin area functions
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
    # Saves all the admin data into the spreadsheet to be checked further
    update_worksheet(data, "admin")
    exit_menu()


welcome_message()
main_user()
