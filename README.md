# **_My Virtual Doctor_**
 
 <a href="https://my-virtual-doctor.herokuapp.com/" target="_blank" rel="noopener">My Virtual Doctor</a>(press for DEMO) is a it is an appointment system for patients and admins.

 # Wireframes
The wireframes for My Virtual Doctor were produced in Lucidchart.
![wireframe](/images/wireframes.png)

# Site Structure

My Virtual Doctor app's purpose is to help patients to book their appointments,change or cancel it.
The information of the user is saved into a spreadsheet on Google drive.

It also gives the option for the admins to assess the patients or send a holiday request which is also stored into the spreadsheet.

# Features
My Virtual Doctor is set up to be easy to use . It contains features that a user would be fimiliar with such as easy keyboard inputs,with instructions for easy and simple experience.

## Existing Features

* ## Heading and Title
* Includes the name of the tool and a brief explanation of what is it used for ,and more importantly how to use it.

![welcome_page](/images/img1.png)

* ## User Area
* Includes the section where all the user details are collected.
* Name, date of birth, calculating age in python, email, symptoms, pick date and time - all with their own personalised validation process to avoid error or app to malfunction.
* NAME input - user should enter 2 names with space between or they will get an error until right input is inserted.
* Date of birth - user should enter a valid date of birth in DD/MM/YYYY format or an error will occur until the right format will be entered.
* Age of the user will be calculated with the date of birth input.
* Email input - user will be asked to enter a valid email with a set regex format , if invalid an error will occur.
* Symptoms description - this is a input personalised message from the user to the doctor whcih will attend his appoinment to know what to expect,if the message is not descriptive enough an error will occur.
* Date of appoinment - should be a date in the future or will turn an error.
* Time of appoinment -should be only 9-18 every day of the week.
* All this data is stored in google spreadsheets.
![user_area](/images/img2.png)
![options](/images/users.png)
![error](/images/error.png)
* ## Admin Area
* Includes a section where admin can log in and has a choice of assessing a patient or putting in a holiday request.
* Please note the password I used is not hidden but this is a future feature that I will include.
* Admin will enter the password and logged in will choose either to assess patient which will take the admin through all the steps above from the user area or to requests section.
* If requests section is chosen Admin will enter his name to be validated.
* The days that admin is working,simple input with comma between or error will occur.
* Also the time admin works daily which has to also be validated.
* Message - is a personalised message from admin to the manager ,it can be holiday request,or any other type of message thathas to be seen by superiors, also has to be descriptive enough or will turn an error.
![admin_area](/images/admins.png)

* ## Changing an appointment
* This section offers the posibility of changing appoinment by collecting the email registered and if it's matching in the spreadsheet it will return details of the appoinment.
* Enter Email - if email does not match any of the emails saved into the spreadsheet error will occur that data is not registered.
* If emails is matched then name ,dob, date and time of appoinment will be displayed .
* Ift will follow steps to take the name , new date of appoinment and new time all have to be validated.
![app_change](/images//dates.png)

# Technologies Used
* Please note that this project is made from a Template from Code Institute and there are aditional languages used only for the purpose of properly running the mock terminal to demostrate this specific project.
* Please note that this app is fully run in terminal so not much styling was used.
* [PYTHON](https://www.w3schools.com/python/) to get details from the user and validate the inputs with python logic.
* [pyfiglet](https://pypi.org/project/pyfiglet/0.7/) to style the welcome message and goodbye greetings.
* [termcolor](https://pypi.org/project/termcolor/) to color the greetings and error messages.

## Browser Compatibility

My Virtual Doctor runs in Heroku terminaland  was tested on the following browsers with no visible issues for the user:
1. Google Chrome 
2. Safari 
3. Mozilla Firefox

# Testing:
* The app was tested in [PEP8](http://pep8online.com).No errors were found.
![Testing](/images/test.png)

# Deployment: 
The site was deployed to Heroku pages.

