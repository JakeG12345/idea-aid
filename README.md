#  PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description:

Idea-AId is a project in the form of a webapp desgned to give inspiration and ideas to people to allow them to test, develop or expand their skills in any genre, field or area. By answering questions through both pre-set and custom responses, users can expand their creativity, learn and find problems to solve. Through the use of openAI's chatGPT-4 API, questions are generated off of previous responses and the five total questions will provide input to GPT-4, which will generate multiple ideas to be used by the user. Each idea can then be expanded upon, again through the help of GPT-4, or saved. 

The users' ID is stored through sessions, and their accout information and ID is stored in a database. Before accessing the generator or their saved ideas, the user must register/ create a new account through the register webpage (register.html) or login through the login webpage (login.html) - with each method having, of course, certain safeguards and restrictions. To create an account, an unused username must be entered (it will be checked against the users database), a password and confirmation must be entered (and must match), and the password must be at least eight characters and contain at least one uppercase letter, lowercase letter and digit. To login, the user must enter their username and password, and they must be valid and match. If, in either case, any of the requirements are not met (or, somehow, a field is returned blank), an appropriate error message will be delivered with the help of the apolog function from helpers.py. After this, the users id will be input into sessions and if they have created an account, the relevant information will be entered into users.db.

After this, the user can...
JAKE PART EVERYTHING U DID EVERY PAGE AND FUNCTION

...
JT PART about saved and its database and its html page
 which stores a users username, password-hash, the date and time the account was created and the 

The static folder contains all relevant files for styling and images - different versions of the logo for use as links, the Atkinson Hyperlegible font, styles.css for general styling (including adjustments for mobile viewing) and nav.css for specific styling of the navbar and its mobile version, with an icon and animated drop-down menu instead of links being displayed on the navbar.