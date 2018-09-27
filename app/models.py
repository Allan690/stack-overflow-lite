from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
ma = Marshmallow()



class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(250), nullable=False)
    date_created = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship(
        'Question', backref=db.backref('questions', lazy='dynamic'))

    def __init__(self, answer, question_id):
        self.answer = answer
        self.question_id = question_id


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Question.query.all()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return "<Question: {}>".format(self.name)



class QuestionSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class AnswerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    question_id = fields.Integer(required=True)
    answer = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
