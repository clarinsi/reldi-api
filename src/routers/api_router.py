
import sys
import xml.etree.ElementTree as ET
from helpers import jsonify, jsonResponse, TCF, jsonTCF, isset
import json

from flask import Blueprint
from flask.ext.cors import CORS
from flask import request
from flask import make_response
from flask import Response


class ServerError(Exception):
    status_code = 500

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

class ApiRouter(Blueprint):
    def __init__(self, dc):
        Blueprint.__init__(self, 'api_router', 'api_router')

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

        @self.route('/')
        def index():
            return "Main"

        @self.errorhandler(ServerError)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response
                
        @self.errorhandler(InvalidUsage)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        @self.errorhandler(Exception)
        def handle_invalid_usage(error):
           response = jsonify(error.message)
           response.status_code = 400
           return response

        @self.route('/<lang>/lexicon', methods=['GET'])
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
            lex = dc.getInstance('lexicon.' + lang)
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

        @self.route('/<lang>/segment', methods=['GET'])
        def segment(lang):
            format = request.args.get('format')
            if not isset(format):
                raise InvalidUsage('Please specify a format', status_code=422)

            text = get_text(format, request)
            segmenter = dc['segmenter.' + lang]

            # Format properly
            result = map(lambda x: map(lambda y: (y,), x), segmenter.segment(text))

            if format == 'json':
                # return jsonify(result)
                return jsonify(jsonTCF(lang, text, result), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result), mimetype='text/xml')

        @self.route('/<lang>/tag', methods=['GET'])
        def tag(lang):
            format = request.args.get('format')
            if not isset(format):
                raise InvalidUsage('Please specify a formatx', status_code=422)

            text = get_text(format, request)
            tagger = dc['tagger.' + lang]
            result = tagger.tag(text)
            if format == 'json':
                print 4
                return jsonify(jsonTCF(lang, text, result, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                print 5
                return Response(TCF(lang, text, result, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/tag_lemmatise', methods=['GET'])
        def tag_lematise(lang):
            format = request.args.get('format')
            if not isset(format):
                raise InvalidUsage('Please specify a format', status_code=422)

            text = get_text(format, request)
            lemmatiser = dc['lemmatiser.' + lang]

            result = lemmatiser.tagLemmatise(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/lemmatise', methods=['GET'])
        def lemmatise(lang):
            format = request.args.get('format')
            if not isset(format):
                raise InvalidUsage('Please specify a format', status_code=422)

            text = get_text(format, request)
            lemmatiser = dc['lemmatiser.' + lang]

            result = lemmatiser.lemmatise(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=1), mimetype='text/xml')
