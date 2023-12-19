import os
from flask import redirect, render_template, session
import datetime
from functools import wraps

def login_required(f): # f is a function, the actual one that will be done like /index or /sell, underneath
    @wraps(f) #this is a function that takes the original function and makes it keep all its metadata
    def decorated_function(*args, **kwargs): #this either makes the original function go to login or what it should be
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(page, message):
    page = page + ".html"
<<<<<<< Updated upstream
    return render_template(page, message=message.title()) #renders the page it came from

def get_question_and_answers(quiz_selections, client):
    past_selections = get_past_selections_str(quiz_selections)
    content = ""
    
    while content.count('::') != 1:
        data = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "user", 
                    "content": f"Query is coming from an app that helps users come up with ideas through the help of AI. It does this through a series of multiple choice questions that lead to a idea. For question {len(quiz_selections) + 1}, give me a question and a few answers. Remember, question should follow past questions to help lead into an idea for the user. Depending on how far along the question, the more or less specific it should be.{past_selections}. IMPORTANT: You should return the question, followed by a '::' (without a space inbetween), followed by the possible answers comma separated without a space inbetween. In other words it should look like 'This is the question?::option 1, another option i guess' and you probably will have more options."
                }
            ]
        )
        content = data.choices[0].message.content
        print("Content:", content)
    
    return content

def get_past_selections_str(quiz_selections):
    past_selections = ""
    
    for selection in quiz_selections:
        past_selections = past_selections + f" - Question: {selection["question"]}, answer: {selection["answer"]}"
    
    if past_selections != "":
        return "Here are past question and answers: " + past_selections
    else:
        return ""
=======
    print(message)
    message = message.title()
    return render_template(page, message=message) #renders the page it came from
>>>>>>> Stashed changes
