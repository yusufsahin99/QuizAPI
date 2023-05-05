from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect
import sqlite3
import os
import pandas as pd

import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions_and_answers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Question(db.Model):
    __tablename__ = 'qa'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(500), nullable=False)
    choice_a = db.Column(db.String(500), nullable=False)
    choice_b = db.Column(db.String(500), nullable=False)
    choice_c = db.Column(db.String(500), nullable=False)
    choice_d = db.Column(db.String(500), nullable=False)
    

    def __repr__(self):
        return f'<Question {self.id}>'

with app.app_context():
    db.create_all()


@app.route('/get_count')
def get_count():
    question = Question.query.order_by(func.random()).first()
    print(repr(question))
    cnt = Question.query.count()
    return {'count' : cnt}
    return render_template('question_template.html', question=question)

@app.route('/get_question')
def get_question():
    question = Question.query.order_by(func.random()).first()
    return render_template('question_template.html', question=question)



def add_question(question_data):
    with app.app_context():
        try:
            question = Question(**question_data)
            db.session.add(question)
            db.session.commit()
        except:
            print('Question could not be added')



if __name__ == '__main__':
    app.run(debug=True)
    





