# -*- coding: utf-8 -*-
import sys
import os
from flask import Flask
from flask.ext.cors import CORS

from src.di import DependencyContainer

from src.api.lexicon import Lexicon
from src.api.segmenter import Segmenter
from src.api.tagger import Tagger
from src.api.lematiser import Lematiser

from src.routers.api_router import ApiRouter
from src.routers.web_router import WebRouter
from src.services.mail_service import MailService
from src.helpers import jsonify

from flask import make_response, redirect

reload(sys)
sys.setdefaultencoding('utf-8')


def init():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/uploads/'

    print app.config['UPLOAD_FOLDER']
    CORS(app)

    print 'Initializing models'
    dc = DependencyContainer(lazy=False)
    for lang in ['hr', 'sl', 'sr']:
        dc['segmenter.' + lang] = lambda: Segmenter(lang)
        dc['tagger.' + lang] = lambda: Tagger(lang, dc['segmenter.' + lang])
        dc['lemmatiser.' + lang] = lambda: Lematiser(lang, dc['segmenter.' + lang], dc['tagger.' + lang])
        dc['lexicon.' + lang] = lambda: Lexicon(lang)

    dc['mail_service'] = lambda: MailService()
    print 'Models initialized'

    api_router = ApiRouter(dc)
    app.register_blueprint(api_router, url_prefix='/api/v1')

    web_router = WebRouter(dc)
    app.register_blueprint(web_router, url_prefix='/web')
    #
    # @app.errorhandler(Exception)
    # def handle_error(error):
    #     '''
    #     @param error:
    #     @type error: string
    #     @return:
    #     @rtype: string
    #     '''
    #     app.logger.error(error)
    #     response = jsonify(error.message)
    #     return response, error.status_code if hasattr(error, 'status_code') else 500

    @app.route('/', methods=['GET'])
    def main():
        return make_response(redirect('/web'))

    return app


def index():
    application = init()
    application.run()

if __name__ == "__main__":

    # text = 'Modeli su učitani! Vrlo uspješno.'

    # lemmatiser = dc['lemmatiser.hr']
    # tagger = dc['tagger.hr']
    # segmenter = dc['segmenter.hr']
    # lexicon = dc['lexicon.hr']

    # print lemmatiser.tagLemmatise(text)
    # print lemmatiser.lemmatise(text)
    # print tagger.tag(text)
    # print segmenter.segment(text)

    app = init()
    app.run(host='0.0.0.0', port=8080, debug=True)
