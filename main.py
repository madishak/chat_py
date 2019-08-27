
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from plyer import notification
from sqlalchemy import select
# from flask import models
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chat.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chat.db')
# app.coSQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
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
    text = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'))



    # def __init__(self, text):
    #     self.text = text.strip()

    def __repr__(self):
        return '<Message %r>' % self.text

#
# class MessageNames():
#     # id = db.Column(db.Integer, primary_key=True)
#     # name = db.Column(db.String(1024), nullable=False)
#     # text = db.Column(db.String(32), nullable=False)
#     def __init__(self, name, text):
#         self.name = [
#             Login(name=n.strip()) for n in name.split(',')
#         ]
#         self.text = [
#             Message(text=t.strip()) for t in text.split(',')
#         ]
#         #super().__init__(name, text)


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
    user = Login(name=name, password=password)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('main', user_id=user.id))

# @app.route('/get_user', methods=['POST'])
# def get_user_id():
#     return add_message(Login.id)

# messages = MessageNames()
# db.session.query(Login, Message).filter(Login.id == Message.id).all()
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', result=db.session.query(Login.name, Message.text).filter(Login.id == Message.user_id).all())


@app.route('/main/<id>', methods=['GET'])
def get_name(id):
    username = request.args.get('user_id')
    # add_message(username)
    return id


@app.route('/add_message', methods=['GET', 'POST'])
def add_message():
    # username = request.args.get('user_id')
    # f = get_name()
    # print(f)
    # print("Madina!!!!!!!!!!!!!!!!!!")
    name = Login.name
    # password = request.form['password']
    text = request.form['message']
    # res=db.session.query(Login.name, Message.text).filter(Login.id == Message.user_id).all()
    users = Login.query.get(37)
    message = Message(text=text, user=users)
    # message = 0
    # for i in res[id]:
    #     print(i)
    #     message = Message(text=text, user=i)



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

    db.session.add(message)
    db.session.commit()

    return redirect(url_for('main'))




if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 5000)

