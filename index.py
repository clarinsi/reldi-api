# -*- coding: utf-8 -*-
import sys
from flask import Flask
from flask.ext.cors import CORS

from src.di import DependencyContainer

from src.api.lexicon import Lexicon
from src.api.segmenter import Segmenter
from src.api.tagger import Tagger
from src.api.lematiser import Lematiser

from src.routers.api_router import ApiRouter
from src.routers.web_router import WebRouter

from flask import make_response, redirect

reload(sys)
sys.setdefaultencoding('utf-8')


def init():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    CORS(app)

    print 'Initializing models'
    dc = DependencyContainer(lazy=False)
    for lang in ['hr', 'sl', 'sr']:
        dc['segmenter.' + lang] = lambda: Segmenter(lang)
        dc['tagger.' + lang] = lambda: Tagger(lang, dc['segmenter.' + lang])
        dc['lemmatiser.' + lang] = lambda: Lematiser(lang, dc['segmenter.' + lang], dc['tagger.' + lang])
        dc['lexicon.' + lang] = lambda: Lexicon(lang)
    print 'Models initialized'

    api_router = ApiRouter(dc)
    app.register_blueprint(api_router, url_prefix='/api/v1')

    web_router = WebRouter(dc)
    app.register_blueprint(web_router, url_prefix='/web')

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



