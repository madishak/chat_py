
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from plyer import notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chat.db'
db = SQLAlchemy(app)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    password = db.Column(db.String(1024), nullable=False)

    def __init__(self, name, password):
        self.name = name.strip()
        self.password = password.strip()
        # self.text = [
        #     Message(text=t.strip()) for t in text.split(',')
        # ]


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    # message_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    # message = db.relationship('Login', backref=db.backref('text', lazy=True))

    def __init__(self, text):
        self.text = text.strip()

    def __repr__(self):
        return '<Message %r>' % self.text


class MessageNames():
    def __init__(self, name, text):
        self.name = [
            Message(text=n.strip()) for n in name.split(',')
        ]
        self.text = [
            Message(text=t.strip()) for t in text.split(',')
        ]
        #super().__init__(name, text)


db.create_all()


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

    db.session.add(Login(name, password))
    db.session.commit()

    return redirect(url_for('main'))

# messages = MessageNames()

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', login=Login.query.all(), messages=Message.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    # name = request.form['nick']
    # password = request.form['password']
    text = request.form['message']


    if len(text) == 0:
        notification.notify(
            title='Ошибка',
            message='Введите сообщение'
        )
        # return
    # elif len(text) == 0:
    #     notification.notify(
    #         title='Ошибка',
    #         message='Введите сообщение'
    #     )
    #     # return

    db.session.add(Message(text))
    db.session.commit()

    return redirect(url_for('main'))


