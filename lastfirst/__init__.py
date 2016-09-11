# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from __future__ import absolute_import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import coaster.app
from coaster.assets import Version
from ._version import __version__

version = Version(__version__)

# First, make an app

app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy(app)

# Second, import the models and views

from . import models, views  # NOQA
from .models import db


# Configure the app
def init_for(env):
    coaster.app.init_app(app, env)
    db.init_app(app)
    db.app = app
