from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from plyer import notification
from datetime import datetime, date, time
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mes.db')
db = SQLAlchemy(app)


class Login(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    messages = db.relationship('Message', backref='user', lazy='dynamic')


    # def __init__(self, name, password):
    #     self.name = name.strip()
    #     self.password = password.strip()
    #     # self.text = [
    #     #     Message(text=t.strip()) for t in text.split(',')
    #     # ]


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(1024), nullable=False)
    text = db.Column(db.String(32), nullable=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'))



    # def __init__(self, text):
    #     self.text = text.strip()

    def __repr__(self):
        return '<Message %r>' % self.date




db.create_all()

current_user = {'user_id': 0}


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', login=Login.query.all())


@app.route('/get_user', methods=['POST'])
def get_user():
    name = request.form['log__name']
    password = request.form['password']
    user = Login(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    current_user['user_id'] = user.id
    return redirect(url_for('main', user_id=current_user['user_id']))


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', result=db.session.query(Login.name, Message.receiver, Message.text, Message.date).filter(Login.id == Message.user_id).all(), login=Login.query.all())


@app.route('/login', methods=['GET'])
def get_names():
    return render_template('main.html', login=Login.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    print(current_user['user_id'])
    print("Madina!!!!!!!!!!!!!!!!!!")
    # name = Login.name

    receiver = request.form.get('receiver')
    text = request.form['message']
    print(receiver)

    current_date = datetime.now(tz=None)
    print(current_date)


    # if current_date < Message.date:
    #     pr

    users = Login.query.get(current_user['user_id'])
    message = Message(receiver=receiver, text=text, date=datetime.now(tz=None), user=users)

    d = Message.query.order_by(db.desc('date')).first()
    print(d)

    r = db.session.query(Login.name, Message.receiver, Message.text, Message.date).filter(Login.id == Message.user_id).filter(Message.receiver == receiver and Message.date > current_date).all()
    print(r)
    if len(text) == 0:
        notification.notify(
            title='Ошибка',
            message='Введите сообщение'
        )

    db.session.add(message)
    db.session.commit()

    return redirect(url_for('main'))




if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 5000)