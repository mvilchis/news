import os

################ Facebook environment variables ################
FACEBOOK_TOKEN = os.getenv("FACEBOOK_TOKEN","")
NEWSPAPER_PAGE="http://www.excelsior.com.mx/"
POSTBACK_MORE="mas_noticias"

##############     Read environment variables     ##############
REDIS_HOST = os.getenv("REDIS_URL","localhost")
REDIS_PORT = 6379
REDIS_URL = "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT)

#############     Configure celery beat          ###############
CELERY_BROKER_URL=REDIS_URL
CELERY_RESULT_BACKEND=REDIS_URL
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Mexico_City'
