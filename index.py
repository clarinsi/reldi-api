# -*- coding: utf-8 -*-
import os
import marshal, types
import sys

# Add all src folders to path
sys.path.append(os.path.realpath('src'))
sys.path.append(os.path.realpath('src/api'))
sys.path.append(os.path.realpath('src/models'))
sys.path.append(os.path.realpath('src/routers'))
import json

import xml.etree.ElementTree as ET
from helpers import jsonify, jsonResponse, TCF, jsonTCF, isset

from flask import Flask
from flask.ext.cors import CORS
from flask import request, make_response, Response, jsonify, session

from auth_token_model import AuthTokenModel

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from DI import DependencyContainer

from lexicon import Lexicon
from segmenter import Segmenter
from tagger import Tagger
from lematiser import Lematiser

from api_router import ApiRouter
from web_router import WebRouter

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)

print 'Initializing models'
dc = DependencyContainer(lazy = True)
for lang in ['hr', 'sl', 'sr']:
    dc['segmenter.' + lang] = lambda: Segmenter(lang)
    dc['tagger.' + lang] = lambda: Tagger(lang, dc['segmenter.' + lang])
    dc['lemmatiser.' + lang] = lambda: Lematiser(lang, dc['segmenter.' + lang], dc['tagger.' + lang])
    dc['lexicon.' + lang] = lambda: Lexicon(lang)

    # Force initialization of models. We want everything initialized before we start serving requests
    tmp = dc['lemmatiser.' + lang]
    tmp = dc['tagger.' + lang]
    tmp = dc['segmenter.' + lang]
    tmp = dc['lexicon.' + lang]

print 'Initialization of models done'

apiRouter = ApiRouter(dc)
app.register_blueprint(apiRouter, url_prefix='/api/v1')
# dc = {}
webRouter = WebRouter(dc)
app.register_blueprint(webRouter, url_prefix='/web')

def index(): 
    app.run()

if __name__ == "__main__":

    text = 'Modeli su učitani! Vrlo uspješno.'

    lemmatiser = dc['lemmatiser.hr']
    tagger = dc['tagger.hr']
    segmenter = dc['segmenter.hr']
    lexicon = dc['lexicon.hr']

    print lemmatiser.tagLemmatise(text)
    print lemmatiser.lemmatise(text)
    print tagger.tag(text)
    print segmenter.segment(text)

    app.run(host='0.0.0.0', port=8080, debug=True)
    


