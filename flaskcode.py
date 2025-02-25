from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# MongoDB Configuration
client = MongoClient('mongodb+srv://listerborn456:<db_password>@cluster0.1a5dn.mongodb.net/')
db = client['contact_app']
users_collection = db['users']
contacts_collection = db['contacts']

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with your email password
mail = Mail(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            return redirect(url_for('contact_form'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        if user:
            # Generate a reset token (for simplicity, just send a message)
            reset_link = "http://localhost:5000/reset_password"  # Replace with actual reset link
            msg = Message('Password Reset', sender='your_email@gmail.com', recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_link}'
            mail.send(msg)
            flash('Password reset link sent to your email', 'success')
        else:
            flash('Email not found', 'error')
    return render_template('forgot_password.html')

@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        reg_number = request.form['reg_number']

        contacts_collection.insert_one({
            'mobile': mobile,
            'email': email,
            'address': address,
            'reg_number': reg_number
        })
        flash('Contact details saved successfully', 'success')
    return render_template('contact_form.html')

@app.route('/search_contact', methods=['GET', 'POST'])
def search_contact():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        contact = contacts_collection.find_one({'reg_number': reg_number})
        if contact:
            return render_template('search_result.html', contact=contact)
        else:
            flash('Contact not found', 'error')
    return render_template('search_contact.html')

if __name__ == '__main__':
    app.run(debug=True)