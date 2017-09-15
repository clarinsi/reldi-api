# -*- coding: utf-8 -*-
import sys
import os
import atexit
from ConfigParser import NoSectionError

from flask import Flask, url_for
from flask.ext.cors import CORS

from src.core.ner_tagger import NerTagger
from src.di import DependencyContainer

from src.core.lexicon import Lexicon
from src.core.segmenter import Segmenter
from src.core.tagger import Tagger
from src.core.lematiser import Lematiser
from src.core.dependency_parser import DependencyParser
from src.core.restorer     import DiacriticRestorer

from src.routers.api_router import ApiRouter, weblicht_get_lang2
from src.routers.web_router import WebRouter
from src.services.mail_service import MailService
from src.helpers import jsonify

from flask import make_response, redirect
from werkzeug.contrib.fixers import ProxyFix

import traceback

reload(sys)
sys.setdefaultencoding('utf-8')

from src.helpers import config

def init():

    languages = ['hr', 'sl', 'sr']

    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/uploads/'

    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    print 'Initializing models'
    dc = DependencyContainer(lazy=False)
    for lang in languages:
        dc['segmenter.' + lang] = lambda: Segmenter(lang)
        dc['tagger.' + lang] = lambda: Tagger(lang, dc['segmenter.' + lang])
        if lang=='sl':
            dc['ner_tagger.' + lang] = lambda: NerTagger(lang, dc['tagger.' + lang])
        dc['lemmatiser.' + lang] = lambda: Lematiser(lang, dc['segmenter.' + lang], dc['tagger.' + lang])
        dc['lexicon.' + lang] = lambda: Lexicon(lang)
        dc['restorer.'+lang] = lambda: DiacriticRestorer(lang, dc['segmenter.' + lang])
        dc['dependency_parser.' + lang] = lambda: DependencyParser(lang, dc['lemmatiser.' + lang])

    dc['mail_service'] = lambda: MailService()

    print 'Models initialized'

    try:
        url_prefix= config.get("url", "prefix")
    except NoSectionError:
        url_prefix=''

    api_router = ApiRouter(dc)
    app.register_blueprint(api_router, url_prefix = url_prefix+'/api/v1')

    web_router = WebRouter(dc)
    app.register_blueprint(web_router, url_prefix = url_prefix+'/web')

    @app.errorhandler(Exception)
    def handle_error(error):
        '''
        @param error:
        @type error: string
        @return:
        @rtype: string
        '''
        app.logger.error(error)
        traceback.print_exc()
        response = jsonify(error.message)
        traceback.print_exc(error)

        return response, error.status_code if hasattr(error, 'status_code') else 500

    @app.route('/', methods=['GET'])
    def main():
        return make_response(redirect(url_prefix+'/web'))

    return app


if __name__ == "__main__":
    text = 'Modeli su učitani! Vrlo uspješno.'

    # lemmatiser = dc['lemmatiser.hr']
    # tagger = dc['tagger.hr']
    # segmenter = dc['segmenter.hr']
    # lexicon = dc['lexicon.hr']

    # print lemmatiser.tagLemmatise(text)
    # print lemmatiser.lemmatise(text)
    # print tagger.tag(text)
    # print segmenter.segment(text)
    weblicht_get_lang2()

    #app = init()
    #app.run(host='0.0.0.0', port=8084) # debug=True, use_reloader=False)
else:
    application = init()
