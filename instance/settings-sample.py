# -*- coding: utf-8 -*-
#: Database backend
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hgapp'
#: Secret key
SECRET_KEY = 'make this something random'
#: Cache type
CACHE_TYPE = 'redis'
#: Timezone
TIMEZONE = 'Asia/Kolkata'
#: Logging: recipients of error emails
ADMINS = []
#: Log file
LOGFILE = 'error.log'
# redis settings for RQ
REDIS_URL = 'redis://localhost:6379/0'
