# -*- coding: utf-8 -*-
import os
import marshal, types
import sys

# Add all src folders to path
sys.path.append(os.path.realpath('src'))
sys.path.append(os.path.realpath('src/api'))
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

    # Force initialization of models. We want everything initialized before we start serving requests
    dc.getInstance('lematiser.' + lang)
    dc.getInstance('tagger.' + lang)
    dc.getInstance('segmenter.' + lang)

print 'Initialization of models done'

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def get_text(format, request):
    if format == 'json':
        return request.args.get('text')
    elif format == 'tcf':
        try:
            return ET.fromstring(request.args.get('text')).text
        except: 
            raise InvalidUsage('Input parameter text is not well formatted')
    else:
        raise InvalidUsage('Unknown format ' + format)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def handle_invalid_usage(error):
   response = jsonify(error.message)
   response.status_code = 400
   return response

@app.route('/api/v1/<lang>/lexicon', methods=['GET'])
def lexicon(lang):

    surface = request.args.get('surface')
    lemma = request.args.get('lemma')
    msd = request.args.get('msd')
    rhymes_with = request.args.get('rhymes_with')
    no_of_syllables = request.args.get('no_of_syllables')
    rhyming_function_bytecode = request.args.get('rhyming_function')
    
    surface = surface if isset(surface) else None
    lemma = lemma if isset(lemma) else None
    msd = msd if isset(msd) else None
    rhymes_with = rhymes_with if isset(rhymes_with) else None
    no_of_syllables = no_of_syllables if isset(no_of_syllables) else None

    if not isset(surface) and not isset(lemma) and not isset(msd):
        raise InvalidUsage('Please specify a surface form, lemma or msd', status_code=422)

    for arg in request.args:
        if arg not in ['surface', 'lemma', 'msd', 'rhymes_with', 'no_of_syllables', 'rhyming_function_bytecode']:
            raise InvalidUsage(arg + ' is an invalid input parameter', status_code=422)

    # if rhyming_function_bytecode is not None:
    #   code = marshal.loads(rhyming_function_bytecode)
    #   func = types.FunctionType(code, globals(), "some_func_name")

    #   return jsonify(func(10, 10))

    lex = Lexicon(lang)
    result = lex.query_entry(surface, lemma, msd, rhymes_with, no_of_syllables)
    return jsonify({
        'query': {
            'surface': surface,
            'lemma': lemma,
            'msd': msd,
            'rhymes_with': rhymes_with,
            'no_of_syllables': no_of_syllables
        },
        'success': True,
        'result': result,
        'count': len(result)
    }, ensure_ascii=False)

@app.route('/api/v1/<lang>/segment', methods=['GET'])
def segment(lang):
    format = request.args.get('format')
    if not isset(format):
        raise InvalidUsage('Please specify a format', status_code=422)

    text = get_text(format, request)
    segmenter = dc.getInstance('segmenter.' + lang)

    # Format properly
    result = map(lambda x: map(lambda y: (y,), x), segmenter.segment(text))

    if format == 'json':
        # return jsonify(result)
        return jsonify(jsonTCF(lang, text, result), ensure_ascii=False)
    elif format == 'tcf':
        return Response(TCF(lang, text, result), mimetype='text/xml')

@app.route('/api/v1/<lang>/tag', methods=['GET'])
def tag(lang):
    format = request.args.get('format')
    if not isset(format):
        raise InvalidUsage('Please specify a format', status_code=422)

    text = get_text(format, request)
    tagger = dc.getInstance('tagger.' + lang)

    result = tagger.tag(text)
    if format == 'json':
        return jsonify(jsonTCF(lang, text, result, tag_idx=1), ensure_ascii=False)
    elif format == 'tcf':
        return Response(TCF(lang, text, result, tag_idx=1), mimetype='text/xml')

@app.route('/api/v1/<lang>/tag_lemmatise', methods=['GET'])
def tag_lematise(lang):
    format = request.args.get('format')
    if not isset(format):
        raise InvalidUsage('Please specify a format', status_code=422)

    text = get_text(format, request)
    tagger = dc.getInstance('tagger.' + lang)

    result = tagger.tagLematise(text)
    if format == 'json':
        return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1), ensure_ascii=False)
    elif format == 'tcf':
        return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')

@app.route('/api/v1/<lang>/lemmatise', methods=['GET'])
def lematise(lang):
    format = request.args.get('format')
    if not isset(format):
        raise InvalidUsage('Please specify a format', status_code=422)

    text = get_text(format, request)
    lematiser = dc.getInstance('lematiser.' + lang)

    result = lematiser.lematise(text)
    if format == 'json':
        return jsonify(jsonTCF(lang, text, result, lemma_idx=1), ensure_ascii=False)
    elif format == 'tcf':
        return Response(TCF(lang, text, result, lemma_idx=1), mimetype='text/xml')

def index(): 
    app.run(debug=True)

if __name__ == "__main__":

    # format = 'json'
    # if not isset(format):
    #     raise ValueError('Please specify a format')
    # lang = 'hr'
    # text = '<text>Modeli su učitani! Vrlo uspješno</text>'

    

    app.run(host='0.0.0.0', port=8080)


