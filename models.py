# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import Column,DateTime, Integer, String


db: SQLAlchemy = SQLAlchemy()


class EmpUser(db.Model):
    __tablename__ = 'emp_user'

    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_username = db.Column(db.String(20), nullable=False)
    emp_password = db.Column(db.String(30), nullable=False)
    emp_level = db.Column(db.Integer, nullable=False)
