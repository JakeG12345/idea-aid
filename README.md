# Idea AId


## Video Demo:  <URL HERE>


## Description:

### Intro
'Idea AId' is a webapp that utilises AI to generate ideas and provide inspiration to people.

### User Authentication
The user's ID is stored through sessions, and their accout information and ID is stored in an SQL (Structured Query Language) database. 

In order to access the generator or saved ideas, the user must be logged in. If not logged in and trying to access one of these pages, the user will be redirected to '/login' which renders 'login.html'. Here they can log in if they have an account. To do this, they must enter their username and password, and they must be valid. If the details are not found in the database (or, somehow, a field is returned blank), an appropriate error message will be delivered with the help of the 'apology' function in 'helpers.py'. After logging in successfully, the users id will be input into session. However, if a user does not have an account, they will need to sign up for one. This can be done at '/register' which renders 'register.html'. To create an account on the register page a few conditions must be met: 
- An unused username must be entered (it will be checked against the 'users' table in the database)
- A password and password confirmation must be entered (they must match)
- The password must be at least eight characters 
- The passwrod must contain at least one uppercase letter, lowercase letter and digit.

If the above conditions are met, the username and password will be added to the 'users' table. The user will also be automatically logged in and hence able to access the generator and the 'Your Ideas' page.

JAKE PART EVERYTHING U DID EVERY PAGE AND FUNCTION

...
JT PART about saved and its database and its html page
 which stores a users username, password-hash, the date and time the account was created and the 

The static folder contains all relevant files for styling and images - different versions of the logo for use as links, the Atkinson Hyperlegible font, styles.css for general styling (including adjustments for mobile viewing) and nav.css for specific styling of the navbar and its mobile version, with an icon and animated drop-down menu instead of links being displayed on the navbar. During the creation of these styles we ran into a few issues - most notable the adjustments we had to make for a mobile interface. To rectify this issue, we used the @media tag to adjust styles based on the size of the suers screen, with the most complicated and, for lack of a better word 'coolest' feature we implemented was the drop-down nav. When on a small screen, the links on the navbar dissapear, leaving just the logo and a hamburger icon. On clicking of the icon an (extremely time consuming to code) animation plays, transforming the hamburger into a X and displaying a drop-down menu with all the links that would be on e traditional navbar.