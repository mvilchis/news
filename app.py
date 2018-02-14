from flask import Flask, jsonify
from threading import Thread

from utils import *
from webargs import fields
from webargs.flaskparser import use_kwargs
app = Flask(__name__)

#############################################################
#                     Restrictions                          #
#############################################################
news_args = {
    'urn': fields.String(required=True),
    'section': fields.String(required=True)
}

location_args = {
    'urn': fields.String(required=True),
    'text': fields.String(required=True)
}

def create_thread_news(urn, text):
    thread = Thread(target = send_news, args=(urn,text))
    thread.start()
    return

def create_thread_location(urn, text):
    thread = Thread(target = send_location, args=(urn,text))
    thread.start()
    return

#############################################################
#                      Endpoints                            #
#############################################################
@app.route("/send_news", methods=['POST', 'GET'])
@use_kwargs(news_args)
def view_send_news(urn, section):
    create_thread_news(section, urn)
    return jsonify({"ok":"ok"})


@app.route("/location", methods=['POST', 'GET'])
@use_kwargs(location_args)
def view_send_news(urn, text):
    create_thread_location(section, text)
    return jsonify({"ok":"ok"})

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))
