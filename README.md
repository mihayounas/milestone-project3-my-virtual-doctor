# **_My Virtual Doctor_**
 
 <a href="https://my-virtual-doctor.herokuapp.com/" target="_blank" rel="noopener">My Virtual Doctor</a>(press for DEMO) is a it is an appointment system for patients and admins.

![wireframe](/images/wireframes.png)

 # Flowchart
The Flowchart for My Virtual Doctor was made in Lucidchart.
![lucidchart](/images/lucid.png)

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

* ## Rescheduling an appointment
* This section offers the posibility of changing appoinment by collecting the email registered and if it's matching in the spreadsheet it will return details of the appoinment.
* Enter Email - if email does not match any of the emails saved into the spreadsheet error will occur that data is not registered.
* If emails is matched then name ,dob, date and time of appoinment will be displayed .
* It will follow steps to take the new date of appoinment and new time all have to be validated.
* All the old data will be deleted and new appoinment will be saved in a different spreadsheet
![app_change](/images/reshh.png)

# Future Features
* As this project is made in pure Python I am planning to style it with CSS.
* Add function to handle the matching emails and return reschedule option.
* Change collect data function into a more cleaner version with the same functions.
* Add more secure log in for the Admin.

# Data Model
I used Google Sheets to store all the data retrieved from My Virtual Doctor.
* Details - used to store user details such as name,date of birth, email,personalised message,date for appoinment and time.
![spredsheet_user](/images/user-spread.png)
* Rescheduled - used to save the old user data as name , date of birth and email and take new data for time and date of appoinment.
![rescheduled-app](/images/resh.png)
* Admin -used to store admin message request ,name ,and shift starting and ending time.
![admin_spreadsheet](/images/spread-adm.png)

# Technologies Used
* Please note that this project is made from a Template from Code Institute and there are aditional languages used only for the purpose of properly running the mock terminal to demostrate this specific project.
* Please note that this app is fully run in terminal so not much styling was used.
* [PYTHON](https://www.w3schools.com/python/) to get details from the user and validate the inputs with python logic.
* [pyfiglet](https://pypi.org/project/pyfiglet/0.7/) to style the welcome message and goodbye greetings.
* [termcolor](https://pypi.org/project/termcolor/) to color the greetings and error messages.


# Testing:
* The app was tested in [PEP8](http://pep8online.com).No errors were found.
![Testing](/images/test.png)

# Manual Testing
The app was tested manually to insure the right functionality and avoid errors.

* Welcome menu : - verify the right input was valid, the input should not be empty space or error on enter.


* User menu -  verify that a name is introduced with space, date of birth should be in the past not in the future and should not be more than 110 years ago,return of the age should be valid, email has a specific regex format, date of appoinment should be only in the future and not in the past,also time of appoinment should be in a timeframe .


* Admin menu - should take the password for admin(password is Admin) - if not valid return to main menu, also should take proper details from admin in order to validate.I made sure none of the steps will take empty spaces or stop at an error.


* Reschedule menu - should match any input email to one already in spreadsheet and return the data saved,if matched should give an option of reschedule or if not matched should give an option to book an appoinment.

Tested manually and made sure that all the data is saved in the corespondent field for better understanding .


# Lighthouse
The website was tested using [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) in Chrome Developer Tools to test each of the pages for:
* Performance - How the page will be loading.
* Accessibility - Checking if the website is  accessible for all users and how can it be improved.
* Best Practices 
* SEO - Search Engine Optimisation. This helps us to understand if the website is optimised for search engine result rankings.
![lighthouse-result](/images/lighthouse.png)

# Browser Compatibility

My Virtual Doctor runs in Heroku terminaland  was tested on the following browsers with no visible issues for the user:
1. Google Chrome 
2. Safari 
3. Mozilla Firefox

# Known bugs:
* If the same email is entered it is not going to say that this email already exists and should retrieve the details.
* I am planning to make a function which will return all the data if the email already exists and give an option to reschedule even thought there already exist a similar function it doesn't do exactly what i would like.

# Deployment: 
The site was deployed to Heroku pages.
1. First we have to create our app on heroku website.
![createapp](/images/createapp1.png)
2. Name the app.
![create2](/images/nameapp2.png)

3. Setup config vars.
![config](/images/setupconfig.png)

4. Select Buildpacks.
![buildpacks](/images/buildpack.png)

5. Choose Deploy Section and Heroku CLI.
![heroku](/images/deploy1.png)

7. Follow the steps bellow.
   To install into terminal:
   Log into heroku : heroku login - i
   * Next command : heroku apps
   * Next command: <app-name> with the actual app name and remove <> : heroku git: remote -a <app_name>
   * Now we have remote control over the app and we can push our changes straight to heroku terminal.
   * MFA/2FA enabled? - click Account setting on heroku website.
                - scroll down to API and click Reveal and Copy the key.
                - command: heroku config and enter api key
                -enter heroku username
                enter api key and press entered.
    After installation I followed the next steps:
![deploy2](/images/deploycli.png)

 # Acknowledgements
The site was completed as a Portfolio 3 Project  (Python)for the Full Stack Software Developer at the [Code Institute](https://codeinstitute.net/). As such I would like to thank my mentor [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/) , Slack community and Code Institute Tutor Support for their help and support.

Mihaela Younas 2022.

