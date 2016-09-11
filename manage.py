#!/usr/bin/env python

from coaster.manage import init_manager

import lastfirst
import lastfirst.models as models
import lastfirst.forms as forms
import lastfirst.views as views
from lastfirst.models import db
from lastfirst import app, init_for


if __name__ == '__main__':
    db.init_app(app)
    manager = init_manager(app, db, init_for, lastfirst=lastfirst, models=models, forms=forms, views=views)
    manager.run()
