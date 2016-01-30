# -*- coding: utf-8 -*-
import os
import marshal, types
import sys

# Add all src folders to path
sys.path.append(os.path.realpath('src'))
sys.path.append(os.path.realpath('src/api'))
sys.path.append(os.path.realpath('src/routers'))
import json

import xml.etree.ElementTree as ET
from helpers import jsonify, jsonResponse, TCF, jsonTCF, isset

from flask import Flask
from flask.ext.cors import CORS
from flask import request
from flask import make_response
from flask import Response
from flask import jsonify
from flask import session

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
CORS(app)

print 'Initializing models'
dc = DependencyContainer(lazy = True)
for lang in ['hr', 'sl', 'sr']:
    dc.registerInstance('lematiser.' + lang, lambda: Lematiser(dc, lang))
    dc.registerInstance('tagger.' + lang, lambda: Tagger(dc, lang))
    dc.registerInstance('segmenter.' + lang, lambda: Segmenter(dc, lang))
    dc.registerInstance('lexicon.' + lang, lambda: Lexicon(dc, lang))

    # Force initialization of models. We want everything initialized before we start serving requests
    dc.getInstance('lematiser.' + lang)
    dc.getInstance('tagger.' + lang)
    dc.getInstance('segmenter.' + lang)
    dc.getInstance('lexicon.' + lang)

print 'Initialization of models done'

apiRouter = ApiRouter(dc)
app.register_blueprint(apiRouter, url_prefix='/api/v1')

webRouter = WebRouter(dc)
app.register_blueprint(webRouter, url_prefix='/web')

def index(): 
    app.run(debug=True)

if __name__ == "__main__":

    # format = 'json'
    # if not isset(format):
    #     raise ValueError('Please specify a format')
    # lang = 'hr'
    # text = '<text>Modeli su učitani! Vrlo uspješno</text>'

    

    app.run(host='0.0.0.0', port=8080)


