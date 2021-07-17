from datetime import date
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:a.yuvAc*@localhost/personal-app'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class AccountInfo(db.Model):
    __tablename__ = 'accountInfo'
    email = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200))
    dateOfBirth = db.Column(db.DateTime(200))
    hobby = db.Column(db.String(200))
    color = db.Column(db.String(200))

    def __init__(self, email, password, dateOfBirth, hobby, color):
        self.email = email
        self.password = password
        self.dateOfBirth = dateOfBirth
        self.hobby = hobby
        self.color = color

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signUp.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = AccountInfo.query.filter_by(email=email, password=password).first()
    if user is None:
        return render_template('login.html', message="You have entered the wrong username or password")
    else:
        return render_template('loggedIn.html', user=user)

@app.route('/createaccount', methods=['POST'])
def createAccount():
    email = request.form['email']
    password = request.form['password']
    dateOfBirth = request.form['dateOfBirth']
    hobby = request.form['hobby']
    color = request.form['color']
    if email == '' or password == '' or dateOfBirth == '' or color == '' or hobby == '':
        return render_template('signUp.html', message='Please enter requiered fileds')
    if db.session.query(AccountInfo).filter(AccountInfo.email == email).count() == 0:
            data = AccountInfo(email, password, dateOfBirth, hobby, color)
            db.session.add(data)
            db.session.commit()
    return render_template('login.html')

if __name__ == '__main__':
    app.run()