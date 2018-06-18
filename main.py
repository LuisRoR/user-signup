from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('index.html', title="Index")

@app.route('/welcome')
def display_welcome_form():
    username = request.args.get('username')
    return render_template('welcome.html', name=username, title='Welcome Page')

def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def is_between_range(min, max, len):
    if len > max or len < min:
        return False
    else:
        return True    

def it_contains_spaces(str):  
    for ch in str:
        if ch.isspace():
            return True
    return False        

@app.route('/validate-signup', methods=['POST'])
def validate_signup():
    username= request.form['username']
    password = request.form['password']
    verify_password = request.form['verify']
    email = request.form['email']
    
    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?" 

    if username == '':
        username_error = "You must enter data in Username field to proceed"
    elif not is_between_range(3,20,len(username)):
        username_error = 'Username value out of range (3-20)'
        username = ''
    else:
        if it_contains_spaces(username):
            username_error = 'Username field contains a space character'
            username = ''
   
    # *** The code below may not be necessary because of the client-side validation
    # *** provided by the use of type='password'. I just wasn't sure of weather to 
    # *** get rid of it or not. I have got a bit confused on the instructions for this
    # *** assignment. However, I believe the input type='password' does not require
    # *** any additional validation. 
    # *** Note: I have tested out and it works either way!
    if password == '':
        password_error = "You must enter data in Password field to proceed"
    elif not is_between_range(3,20,len(password)):
        password_error = 'Password value out of range (3-20)'
    else:
        if it_contains_spaces(password):
            password_error = 'Password field contains a space character'

    if verify_password == '':
        verify_password_error = "You must enter data in Verify password field to proceed"
    elif not is_between_range(3,20,len(verify_password)):
        verify_password_error = 'Verify password value out of range (3-20)'
    elif it_contains_spaces(verify_password):
        verify_password_error = 'Verify password field contains a space character'
    else:     
        if password != verify_password:
            verify_password_error = 'The password and password-confirmation do not match'
    # *** End of block using type='password' attribute.  

    if email != '':
        if not is_between_range(3,20,len(email)): 
            email_error = 'Email value out of range (3-20)' 
        elif it_contains_spaces(username):
                email_error = 'Email field contains a space character'       
        else:
            if not re.match(pattern, email):
                email_error = 'Invalid email. Only a single "@" and a single "." and not spaces allowed. Lenght between 3-20 charcters.'
                

    if not username_error and not password_error and not verify_password_error and not email_error:
        #succes
        return redirect('/welcome?username={0}'.format(username))
    else:
        password = '' 
        verify_password = '' 
        return render_template('index.html', 
            username_error = username_error, 
            password_error = password_error, 
            verify_password_error = verify_password_error, 
            email_error = email_error,
            username = username,
            password = password,
            verify_password = verify_password,
            email = email, 
            title = "Index"
            )
    

app.run()