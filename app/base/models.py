
# Flask
from enum import unique
from re import I
from flask_login import UserMixin

# SQL-Alchemy
from sqlalchemy import Column, String, Integer, LargeBinary, JSON, DateTime, Boolean, Float
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey

# 'app' Folder
from app import db, login_manager
from app.base.util import hash_pass

# Other modules
from datetime import datetime

from marshmallow import validate
from marshmallow_jsonapi import Schema, fields

NOT_BLANK = validate.Length(min=1, error='Field cannot be blank')

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)      # Email
    username = Column(String, unique=True)   # Username
    password = Column(LargeBinary)           # Password (Hashed Binary)
    role = Column(String, default='Regular') # Admin || Regular

    credits = Column(Integer, default=0)
    messages_sent_total = Column(Integer, default=0)
    messages_sent_month = Column(Integer, default=0)
    subscription = Column(String, default="Free")
    subscription_credits = Column(Integer, default=1000)
    access_code = Column(String)

    licenses = Column(Integer, default=0)
    activated_licenses = Column(Integer, default=0)

    theme_preference = Column(String, default='Dark')
    color_preference = Column(String, default='primary')
    sidebar_preference = Column(String, default='minimal')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass( value )
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class AccessCodes(db.Model):

    __tablename__ = 'accesscodes'

    id = Column(Integer, primary_key=True)
    access_code = Column(String)
    access_permissions = Column(String, default="Admin")
    username = Column(String, default="")
    email = Column(String, default="")

class NewTweetCheck(db.Model):

    __tablename__ = 'newtweetcheck'

    id = Column(Integer, primary_key=True)
    new_tweet = Column(String)
    tweet_data = Column(JSON)





#### TOKEN AND TWITTER ####
class Follower(db.Model):
    __tablename__ = 'follower'

    id                  = Column(Integer)
    user_id             = Column(String(255), unique=True, primary_key=True )
    date_followed       = Column(DateTime(timezone=True), unique=False, default=datetime.now())
    name                = Column(String(255), unique=False)
    follower_count      = Column(Integer,     unique=False)
    screen_name         = Column(String(255), unique=False)
    profile_banner_url  = Column(String(),    unique=False)
    profile_image_url   = Column(String(),    unique=False)
    verified            = Column(Boolean,     unique=False)
    following           = Column(Boolean,     unique=False)
    tokens_tweeted      = Column(Integer(),   unique=False)
    average_h_performance = Column(Float(),         unique=False)
    average_two_h_performance = Column(Float(),     unique=False)
    average_three_h_performance = Column(Float(),   unique=False)
    average_four_h_performance = Column(Float(),    unique=False)
    average_twelve_h_performance = Column(Float(),  unique=False)
    average_day_performance = Column(Float(),       unique=False)

class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(String(255), unique=False)
    name = Column(String(255), unique=False)
    user_id = Column(String(255), unique=False)
    tweet = Column(String(255), unique=False)
    datetime = Column(DateTime(timezone=True), unique=False)
    token = Column(String(255), unique=False)
    pair_id = Column(String(255), unique=False)
    token_name = Column(String(255), unique=False)
    price_at_tweet = Column(Float(), unique=False)
    prices = Column(JSON, unique=False, default={
        '0': None, '1': None, '2': None, '3': None, '4': None, '12': None, '24': None
    }) # filled out with hourly prices => {1: 2.78, 2: 3.23, 3: 2.82, ... 24: 5.53}
    token_price_collection_complete = Column(Boolean, unique=False)
    collection_attempts = Column(Integer, unique=False, default=0)




### JSON SCHEMAS ###

class TweetSchema(Schema):
    # Validation for the different fields
    id                  = fields.Integer(validate=NOT_BLANK)
    tweet_id            = fields.String(validate=NOT_BLANK)
    pair_id             = fields.String(validate=NOT_BLANK)
    datetime            = fields.DateTime(validate=NOT_BLANK)
    user_id             = fields.String(validate=NOT_BLANK)

    class Meta:
        type_ = 'tweet'

### JSON SCHEMAS ###




# Manages user authentication
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None