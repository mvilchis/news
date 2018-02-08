from flask import Flask, jsonify

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


#############################################################
#                      Endpoints                            #
#############################################################
@app.route("/send_news", methods=['POST', 'GET'])
@use_kwargs(news_args)
def view_send_news(urn, section):
    send_news(section, urn)
    return jsonify({"ok":"ok"})

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))
