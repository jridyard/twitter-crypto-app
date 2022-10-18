from distutils.log import debug
from functools import wraps
from tokenize import group
from base64 import b64encode
import json
from urllib import parse as urlparse
from discord_webhook import DiscordWebhook

from flask_cors import CORS, cross_origin
import requests

# Database (MODELS)
from app.base.models import *

# SQL-Alchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

# Flask, Jinja
from flask import Flask, Response, render_template, redirect, url_for, make_response, jsonify, request
from flask_login import login_required, current_user
from flask_migrate import current
from jinja2 import TemplateNotFound

# 'app' Folder
from app import login_manager
from app import db
from app import tasks
from app.home import blueprint

# 'functions' Folder
from app.home.functions.basic_function import basic

# Other modules
from time import sleep
import tweepy

from datetime import datetime, timedelta

from app.home.twitter_api import *

def getTimeStamp(time):
    return int(datetime.timestamp(time))