
import sys
import xml.etree.ElementTree as ET
from ..helpers import jsonify, TCF, jsonTCF, isset
from lxml import etree
from StringIO import StringIO

from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app
from functools import wraps
from ..models.user_model import UserModel
from ..models.auth_token_model import AuthTokenModel


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


class Unauthorized(Exception):
    status_code = 401

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

        def authenticate(api_method):
            def error_message(message):
                return jsonify({
                    'success': False,
                    'result': [],
                    'count': 0,
                    'message': message
                }, ensure_ascii=False)

            @wraps(api_method)
            def verify(*args, **kwargs):
                auth_token_string = request.cookies.get('auth-token')
                if auth_token_string is None:
                    auth_token_string = request.headers.get('Authorization')

                authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
                if authToken is None or not authToken.isValid():
                    raise Unauthorized('Invalid token')

                # Log request
                user = UserModel.getByPk(authToken.user_id)
                if user is None:
                    raise Unauthorized('Invalid token')
                
                user.logRequest()
                user.save()
                return api_method(*args, **kwargs)
                
            return verify

        def get_text(format, request):
            if format == 'json':
                return request.args.get('text')
            elif format == 'tcf':
                with open('assets/tcfschema/d-spin-local_0_4.rng', 'r') as f:
                    relaxng_doc = etree.parse(f)
                    relaxng = etree.RelaxNG(relaxng_doc)
                    doc = etree.parse(StringIO(request.args.get('text').encode('utf-8')))
                    if relaxng.validate(doc):
                        return 'Modeli su zakon'
                    else:
                        raise InvalidUsage('Input xml does not comply to TCF schema')
            else:
                raise InvalidUsage('Unknown format ' + format)

        @self.route('/')
        def index():
            return "Main"

        @self.errorhandler(Exception)
        def handle_error(error):
            current_app.logger.error(error)
            response = jsonify(error.message)
            return response

        @self.route('/<lang>/lexicon', methods=['GET'])
        @authenticate
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
            lex = dc['lexicon.' + lang]
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
        @authenticate
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
        @authenticate
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
        @authenticate
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
        @authenticate
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
