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
from datetime import datetime
import time
import re
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
            'if you have an appoinment press "h" to check your history:\n'
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
        if admin_or_patient == 'h':
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
    continue_menu()
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
        regex_name = re.compile(
            r'^([a-z]+)( [a-z]+)+( [a-z]+)*( [a-z]+)*$', re.IGNORECASE
            )
        re_format_check = regex_name.search(names)
        # If match is found, the string is valid
        if re_format_check:
            print("Name is Valid...saving")
            return names
        # If match is not found, string is invalid
        else:
            print(
                colored(
                    "Not valid please enter First and Last name separated by"
                    " space...",
                    'red')
                    )
    return True


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
            "format DD/MM/YYYY or press 'e' to exit:\n"
        )
        e_for_exit(date_input)
        format_str = "%d/%m/%Y"
        try:
            datetime.strptime(date_input, format_str)
            day, month, year = date_input.split('/')
            birth_date = datetime(int(year), int(month), int(day))
            # Calculates age in years for the patient
            age_years = (datetime.now() - birth_date)
            convertdays = int(age_years.days)
            age_years = int(convertdays/365)
            # It won't take anything later than 100 years old
            if age_years <= 0:
                print(
                    colored(
                        "The year you entered is invalid,please try again...\n"
                        "The date entered is in the future...\n",
                        'red')
                        )
                continue
            if age_years < 100:
                print("Saving DOB...")
                print(f"You are {age_years} years old.")
                return date_input
            else:
                print(
                    colored(
                        "The year you entered is invalid,please try again...\n"
                        "The year you entered is too far in the past...\n",
                        'red')
                        )
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
        email_val = input(
            "Please enter a valid email address or 'e' to exit:"
            "\n"
        )
        e_for_exit(email_val)
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
        symptoms_val = input(
            "Please enter you symptoms bellow or 'e' to exit:"
            "\n"
            )
        e_for_exit(symptoms_val)
        # Only accept a proper message description
        regex_mess = re.compile(
            r'^([a-z]+)( [a-z]+)+( [a-z]+)( [a-z]+)( [a-z]+)*$', re.IGNORECASE
            )
        re_format_check = regex_mess.search(symptoms_val)
        # If match is found, the string is valid
        if re_format_check:
            print("Thank you...saving...")
            return symptoms_val
        # If match is not found, string is invalid
        else:
            print(
                colored(
                    "Not valid,please try to enter more details...",
                    'red')
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
        now = datetime.now()
        try:
            # convert to string
            date_time_str = now.strftime("%d/%m/%Y")
            print("Please choose a date later than today's date.")
            print(colored("This is today's date: " + date_time_str, 'yellow'))
            date_user_input = input(
                "Please enter your appoinment date DD/MM/YYYY or 'e' to exit:"
                "\n"
            )
            e_for_exit(date_user_input)
            date1 = time.strptime(date_user_input, "%d/%m/%Y")
            date2 = time.strptime(date_time_str, "%d/%m/%Y")
            if date1 > date2:
                print("Valid date...saving...")
                return date_user_input
            else:
                print(
                    colored(
                        "Invalid,please choose a date in the future...", 'red'
                        )
                        )
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
        time_val = input(
            "Please enter a time between 9 - 18 or 'e' to exit..."
            "\n"
            )
        e_for_exit(time_val)
        try:
            if int(time_val) in range(9, 19):
                print("Time is valid...saving...")
                return time_val
            else:
                print(
                    colored(
                        "This is not valid,choose a time between 9-18..."
                        "please try again...",
                        'red')
                        )
                continue
        except ValueError:
            print(
                colored(
                    "This is not valid,choose a time between 9-18..."
                    "please try again...",
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
                "To register a patient press 'a' or 's' to manage shift...\n"
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
            print("Invalid,please enter a descriptive message...")
    return True


# Gives option to on to the main menu or exit screen
def continue_menu():
    """
    This menu will offer a choice to user,
    he can continue entering his details or exit.
    """
    print("-" * 80)
    while True:
        menu_exit = input(
            colored(
                "If you would like to continue press 'c' or 'e' to go back "
                "to main menu...\n", 'blue'
                )
                )
        if menu_exit == "c":
            break
        if menu_exit == 'e':
            print(colored("Exiting...", 'red'))
            welcome_message()
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
    while True:
        exit_choice = input(
            "To go back to main menu press 'm' or 'e' to exit:\n"
            )
        if exit_choice == "m":
            welcome_message()
            main_user()
        if exit_choice == 'e':
            text = "GoodBye...\n"
            welcome_msg(text)
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


# Collect the data already save into the spreadsheet
def collect_data():
    """
    Displays data for the user in order to allow them
    to cancel or change their appoinment
    """
    print("Here you will be able to check your appoinment details.")
    print(
        "Your email has to match to the one you used to book your"
        " appoinment..."
    )
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
            register_choice = input(
                "Please press 'm' for main menu or 'e' to exit:"
                )
            if register_choice == 'm':
                welcome_message()
            if register_choice == 'e':
                e_for_exit(register_choice)
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
    # Offers option to reschedule or change the appoinment
    print(
        colored(
            "Reschedule process will remove the existing appoinment and"
            " create a new one...", 'red'
            )
            )
    cancel_return = input(
        "To reschedule your appointment press 'r' or 'm' for main menu:\n"
        )
    if cancel_return == 'r':
        print("Please enter your new details...")
        # Deletes all the data entered for the old appoinment from the
        # spreadsheet.
        details = SHEET.worksheet('details')
        details.delete_rows(name_row)
        new_data()
    if cancel_return == 'm':
        main_user()


# Collects new details for a new appoinment
def new_data():
    """
    Collects new data and saves it into a different
    spreadsheet.
    """
    name_new = get_name()
    date_new = pick_a_date()
    time_new = get_time()
    new_email = get_email()
    new_dob = get_birth_date()
    new_info = [name_new, date_new, time_new, new_email, new_dob]
    update_worksheet(new_info, 'rescheduled')
    print(
        f"You appoinment was now rescheduled on {date_new} at {time_new}."
        )


def book_one_more():
    """
    Gives option to book one more appoinment or exit
    the app.
    """
    one_more_app = input(
        "If you would like to book another appointment please press 'b' or 'e'"
        " to exit to main menu"
        )
    if one_more_app == 'b':
        main_user()
    if one_more_app == 'e':
        welcome_message()
        main_user()


# This function will offer the chance to restart the booking
# process in case that user changes their mind or makes a mistake.
def e_for_exit(input_choice):
    """
    This function gives the option to exit and leave the process
    of the booking if user changed their mind.
    """
    if input_choice == 'e':
        welcome_message()


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
        f'{time_user}:00'
        ]
    update_worksheet(data, 'details')
    book_one_more()
    exit_screen()


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
    continue_menu()


welcome_message()
main_user()
