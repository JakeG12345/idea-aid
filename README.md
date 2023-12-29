# Idea AId


## Video Demo:  <URL HERE>


## Description:

### Breif Description
'Idea AId' is a webapp that utilises AI to generate ideas and provide inspiration to people. It was created using Flask, HTML, Python, CSS, SQL, the OpenAI API and Bootstrap.



### User Authentication
The user's ID is stored through sessions, and their accout information and ID is stored in an SQL (Structured Query Language) database. 

In order to access the generator or saved ideas, the user must be logged in. If not logged in and trying to access one of these pages, the user will be redirected to '/login' which renders 'login.html'. Here they can log in if they have an account. To do this, they must enter their username and password, and they must be valid. If the details are not found in the database (or, somehow, a field is returned blank), an appropriate error message will be delivered with the help of the 'apology' function in 'helpers.py'. After logging in successfully, the users id will be input into session. However, if a user does not have an account, they will need to sign up for one. This can be done at '/register' which renders 'register.html'. To create an account on the register page a few conditions must be met: 
- An unused username must be entered (it will be checked against the 'users' table in the database)
- A password and password confirmation must be entered (they must match)
- The password must be at least 8 characters 
- The password must contain at least 1 uppercase letter, lowercase letter and digit.

If the above conditions are met, the username and password will be added to the 'users' table. The user will also be automatically logged in and hence able to access the generator and the 'Your Ideas' page.



### The Generator
When a user goes to '/generator' they are prompted with a question that is likely very generic like 'What is the primary goal of your project or idea?'. This question has been generated from ChatGPT-4-Turbo through the OpenAI API. The query sent to OpenAI specifies for the bot to return a question and possible options with special syntax so that it can be parsed. The parsed data is then provided to the HTML via Jinja2 and displayed. There is also a custom answer box which users can use to answer the question. After pressing one of the options or submitting a custom option, the user's answer is posted to '/generator' where it is stored in a variable that keeps track of the selections (a list of the questions, options and answers). Then, ChatGPT is queried again through the 'get_question_and_answers' function in 'helpers.py' with the first question and answer indicating that the bot provides another question and options. This process repeats, with the questions getting more and more specific as more data is gathered. Once 5 questions have been asked, a function called 'get_ideas()' in helpers.py is called that as indicated in the name, gets ideas. It takes in the selections variable as an argument and uses that to get creative ideas from ChatGPT that would suit the user. This data is then feeded to the HTML and displayed. When a user clicks on an idea, they have 2 options:
- 'Save' (saves idea as further discussed in idea saving section), or if the idea is saved, 'remove from saved' (removes idea from saved as further discussed in idea saving section)
- 'Expand' (navigates user to expand page providing idea title as further discussed in expand section)



### Idea Saving
In the SQL database, there is an ideas table with the following fields: userID, title, date_edited and ideaID (the primary key). The table is used to track saved ideas among all users.

An idea can be saved from two places: '/generator' or '/expand'. Upon pressing the save button for an idea, the user is directed to '/generator' or '/expand' (depending on the page on) providing POST data with a field 'save-idea' that contains the idea title. The server then checks for the 'save-idea' field in the posted form and if found, will save the idea’s title, current user ID, and date to the database. After that, the page is rerendered and will display a delete or remove from saved option where the save button originally was.

A user can also delete ideas, which functionally is done in a similar way to saving ideas. This can be done on '/generator', '/expand' and '/saved'. When recieving a POST request, these destinations' functions check for a 'remove-idea' field. It then removes that idea title provided in 'remove-idea' on the database and rerenders the page, changing it depending on the idea removed.

Visiting the '/saved' route will render 'saved.html' - a page that displays saved ideas. On this page, there is a table with columns for the idea, the date and time it was saved, a button to expand the idea, and a remove button. The expand button POSTs the title of the idea to the expand path which then renders the expand page for the idea selected (further discussed in expand section).



### Expand
The expand page located at '/expand' provides users with a detailed explanation of an idea and some similar ideas. It also allows users to save the idea or remove it from saved ideas if it is already saved.

When a user is directed to '/expand', they POST the title of the idea to the server in a field called 'idea'. This idea is read by the server and provided to two ChatGPT queries: one for the detailed description, and the other for similar ideas. This data is then provided to the HTML through the render_template function and displayed on the screen.



### Styling
The static folder contains all relevant files for styling and images, these including:
- Different versions of the logo for use as links
- The Atkinson Hyperlegible font
- 'styles.css' for general styling (including adjustments for mobile viewing)
- 'nav.css' for specific styling of the navbar and its mobile version - featuring a hamburger-icon and animated drop-down menu instead of a horizontal display of links as seen on the desktop navbar.

During the creation of these styles we ran into a few issues - most notably the adjustments we had to make for a mobile interface. To rectify this issue, we used the @media tag to adjust styles based on the size of the users screen, with the most complicated and, for lack of a better word 'coolest' stylistic feature we implemented being the drop-down nav menu for mobile. When on a small screen, the links on the navbar dissapear, leaving just the logo and a hamburger icon. On pressing the hamburger-icon, an (extremely time consuming to code) animation plays, transforming the hamburger into an 'X' and displaying a drop-down menu with all the links that would be on the desktop navbar.

Aside from CSS, some Bootstrap was used. For instance, it was used to create the table of saved ideas on '/saved'.