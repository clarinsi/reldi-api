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
import re, os, json, csv, traceback


class ServerError(Exception):
    """
    Thrown during a 500 server error
    """
    status_code = 500

    def __init__(self, message):
        '''
        @param message: The exception message to be shown
        @type message: string
        '''
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        '''

        @return:
        @rtype: string
        '''
        rv = dict()
        rv['message'] = self.message
        return rv


class Unauthorized(Exception):
    """
    Thrown during a 401 server error
    """
    status_code = 401

    def __init__(self, message):
        '''
        @param message: The exception message to be shown
        @type message: string

        '''
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        '''
        @return:
        @rtype: string
        '''
        rv = dict()
        rv['message'] = self.message
        return rv


class InvalidUsage(Exception):
    """
    Thrown during a 422 server error
    """
    status_code = 422

    def __init__(self, message):
        '''
        @param message:
        @type message: string
        '''
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        '''

        @return:
        @rtype: string
        '''
        rv = dict()
        rv['message'] = self.message
        return rv

class BadRequest(Exception):
    """
    Thrown during a 422 server error
    """
    status_code = 400

    def __init__(self, message):
        '''
        @param message:
        @type message: string
        '''
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        '''

        @return:
        @rtype: string
        '''
        rv = dict()
        rv['message'] = self.message
        return rv


class ApiRouter(Blueprint):
    def register(self, app, options, first_registration=False):
        super(ApiRouter, self).register(app, options, first_registration=False)
        self.config = app.config

    def __init__(self, dc):
        '''Routes HTTP requests to specific calls to the internal core/api classes

        @param dc: dependency injection container with initialized core objects
        @type dc: DependencyContainer
        '''
        Blueprint.__init__(self, 'api_router', 'api_router')
        self.config = {}

        def authenticate(api_method):
            '''
            The method is executed before each HTTP API call.
            If a valid cookie or authentication header is not set, an Unauthorized Exception will be thrown.

            @param api_method:
            @type api_method: string
            @return:
            @rtype: string
            '''

            @wraps(api_method)
            def verify(*args, **kwargs):
                '''

                @param args:
                @type args: string
                @param kwargs:
                @type kwargs: string
                @return:
                @rtype: string
                '''
                auth_token_string = request.cookies.get('auth-token')
                if auth_token_string is None:
                    auth_token_string = request.headers.get('Authorization')

                if auth_token_string is None:
                    raise Unauthorized('Invalid token')

                authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
                if authToken is None or not authToken.isValid():
                    raise Unauthorized('Invalid token')

                # Log request
                user = UserModel.getByPk(authToken.user_id)
                if user is None:
                    raise Unauthorized('Invalid token')

                if user.status != 'active':
                    raise Unauthorized('User has no access')

                user.logRequest()
                user.save()
                return api_method(*args, **kwargs)

            return verify

        def save_file(api_method):
            @wraps(api_method)
            def post_request(*args, **kwargs):
                auth_token_string = request.cookies.get('auth-token')
                if auth_token_string is None:
                    auth_token_string = request.headers.get('Authorization')

                if auth_token_string is None:
                    raise Unauthorized('Invalid token')

                authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
                if authToken is None or not authToken.isValid():
                    raise Unauthorized('Invalid token')

                result = api_method(*args, **kwargs)
                filePath = os.path.join(self.config['UPLOAD_FOLDER'], get_request_id(request))

                raw = result.get_data()
                try:
                    data = json.loads(raw)
                    csvResult = []
                    posTags = {}
                    lemmas = {}
                    tokens = {}
                    parse = {}

                    if 'POStags' in data:
                        for tag in data['POStags']['tag']:
                            posTags[tag['tokenIDs']] = tag

                    if 'lemmas' in data:
                        for lemma in data['lemmas']['lemma']:
                            lemmas[lemma['tokenIDs']] = lemma

                    if 'tokens' in data:
                        for token in data['tokens']['token']:
                            tokens[token['ID']] = token

                    if 'depparsing' in data:
                        previousTokenSum = 0
                        for sentence in data['depparsing']['parse']:
                            for token in sentence['dependency']:
                                if 'govIDs' in token:
                                    parse[token['depIDs']] = {
                                        'govIDs': int(token['govIDs'].split('_')[1]) - previousTokenSum + 1,
                                        'func': token['func']
                                    }
                                else:
                                    parse[token['depIDs']] = {
                                        'govIDs': '0',
                                        'func': 'root'
                                    }
                            previousTokenSum += len(sentence['dependency'])

                    for sentence in data['sentences']['sentence']:
                        for idx, tid in enumerate(sentence['tokenIDs'].split(' ')):
                            csvResult.append([])
                            token = tokens[tid]
                            csvResult[-1].append(idx + 1)
                            csvResult[-1].append(token['text'])

                            if tid in posTags:
                                csvResult[-1].append(posTags[tid]['text'])
                            if tid in lemmas:
                                csvResult[-1].append(lemmas[tid]['text'])
                            if tid in parse:
                                csvResult[-1].append(parse[tid]['govIDs'])
                                csvResult[-1].append(parse[tid]['func'])

                            csvResult[-1].append(token['startChar'])
                            csvResult[-1].append(token['endChar'])

                        csvResult.append([])

                    with open(filePath, 'w') as f:
                        w = csv.writer(f, delimiter="\t")
                        w.writerows(csvResult)

                except:
                    with open(filePath, 'w') as f:
                        f.write(raw)

                return result

            return post_request

        def get_format(request):
            params = request.form if request.method == 'POST' else request.args
            format = params.get('format')
            return format

        def get_request_id(request):
            params = request.form if request.method == 'POST' else request.args
            request_id = params.get('request-id')
            if not isset(request_id):
                raise InvalidUsage('Please specify a request id')

            return request_id

        def weblicht_get_text(request):
            with open('assets/tcfschema/d-spin-local_0_4.rng', 'r') as f:
                text = request.data
                relaxng_doc = etree.parse(f)
                relaxng = etree.RelaxNG(relaxng_doc)
                inputXml = re.sub(">\\s*<", "><", text)
                inputXml = re.sub("^\\s*<", "<", inputXml)

                doc = etree.parse(StringIO(inputXml))
                try:
                    relaxng.assertValid(doc)
                    return doc.getroot()[1][0].text
                except Exception as e:
                    raise InvalidUsage(e.message)

        def get_text(format, request):
            '''

            @param format:
            @type format: string
            @param request:
            @type request: string
            @return:
            @rtype: string
            '''
            params = request.form if request.method == 'POST' else request.args
            files = request.files
            if format == 'json':
                if 'file' in files:
                    return files['file'].read()
                else:
                    return params.get('text')
            elif format == 'tcf':
                with open('assets/tcfschema/d-spin-local_0_4.rng', 'r') as f:

                    if 'file' in files:
                        text = files['file'].read()
                    else:
                        text = params.get('text').encode('utf-8')
                    relaxng_doc = etree.parse(f)
                    relaxng = etree.RelaxNG(relaxng_doc)
                    inputXml = re.sub(">\\s*<", "><", text)
                    inputXml = re.sub("^\\s*<", "<", inputXml)

                    doc = etree.parse(StringIO(inputXml))
                    try:
                        relaxng.assertValid(doc)
                        return doc.getroot()[1][0].text
                    except Exception as e:
                        raise InvalidUsage(e.message)
            else:
                raise InvalidUsage('Unknown format ' + format)

        @self.route('/')
        def index():
            '''

            @return:
            @rtype: string
            '''
            return "Main"

        @self.errorhandler(Exception)
        def handle_error(error):
            '''

            @param error:
            @type error: string
            @return:
            @rtype: string
            '''
            current_app.logger.error(error)
            response = jsonify(error.message)
            return response, error.status_code if hasattr(error, 'status_code') else 500

        @self.route('/<lang>/lexicon', methods=['GET', 'POST'])
        @authenticate
        def lexicon(lang):
            """

            Parameters
            ----------
            lang

            Returns
            -------

            """
            input_parameters = ['surface', 'lemma', 'msd', 'rhymes_with',
                                'no_of_syllables', 'rhyming_function_bytecode',
                                'surface_is_regex', 'lemma_is_regex', 'msd_is_regex', 'request-id']

            surface = request.args.get('surface')
            lemma = request.args.get('lemma')
            msd = request.args.get('msd')
            rhymes_with = request.args.get('rhymes_with')
            no_of_syllables = request.args.get('no_of_syllables')
            rhyming_function_bytecode = request.args.get('rhyming_function')
            surface_is_regex = (request.args.get('surface_is_regex') == "1")
            lemma_is_regex = (request.args.get('lemma_is_regex') == "1")
            msd_is_regex = (request.args.get('msd_is_regex') == "1")

            surface = surface if isset(surface) else None
            lemma = lemma if isset(lemma) else None
            msd = msd if isset(msd) else None
            rhymes_with = rhymes_with if isset(rhymes_with) else None
            no_of_syllables = no_of_syllables if isset(no_of_syllables) else None

            if not isset(surface) and not isset(lemma) and not isset(msd) and not isset(rhymes_with) and not isset(
                    no_of_syllables):
                raise InvalidUsage('Please specify a surface form, lemma or msd')

            for arg in request.args:
                if arg not in input_parameters:
                    raise InvalidUsage(arg + ' is an invalid input parameter')

            # if rhyming_function_bytecode is not None:
            #   code = marshal.loads(rhyming_function_bytecode)
            #   func = types.FunctionType(code, globals(), "some_func_name")

            #   return jsonify(func(10, 10))

            lex = dc['lexicon.' + lang]
            """:type : Lexicon """
            result = lex.query_entry(surface, lemma, msd, rhymes_with, no_of_syllables,
                                     surface_is_regex, msd_is_regex, lemma_is_regex)

            return jsonify({
                'query': {
                    'surface': surface,
                    'lemma': lemma,
                    'msd': msd,
                    'rhymes_with': rhymes_with,
                    'no_of_syllables': no_of_syllables
                },
                'success': True,
                'language': lex.language,
                'result': result,
                'count': len(result)
            }, ensure_ascii=False)

        @self.route('/<lang>/segment', methods=['GET', 'POST'])
        @authenticate
        def segment(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            segmenter = dc['segmenter.' + lang]

            # Format properly
            result = map(lambda x: map(lambda y: (y,), x), segmenter.segment(text))

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result), mimetype='text/xml')

        @self.route('/<lang>/restore', methods=['GET', 'POST'])
        @authenticate
        def restore(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            restorer = dc['restorer.' + lang]
            result = restorer.restore(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, correction_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, correction_idx=1), mimetype='text/xml')

        @self.route('/<lang>/tag', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''

            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            tagger = dc['tagger.' + lang]
            result = tagger.tag(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, tag_idx=1), mimetype='text/xml')


        @self.route('/weblicht/<lang>/tag_lemmatise', methods=['GET', 'POST'])
        def weblicht_tag_lemmatise(lang):
            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            lemmatiser = dc['lemmatiser.' + lang]
            result = lemmatiser.tagLemmatise(text)
            return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/tag_lemmatise', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag_lematise(lang):
            '''

            @return:
            @rtype:
            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            lemmatiser = dc['lemmatiser.' + lang]

            result = lemmatiser.tagLemmatise(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/lemmatise', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def lemmatise(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            lemmatiser = dc['lemmatiser.' + lang]

            result = lemmatiser.lemmatise(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=1), mimetype='text/xml')

        @self.route('/<lang>/tag_lemmatise_depparse', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag_lemmatise_depparse(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            dependency_parser = dc['dependency_parser.' + lang]

            result = dependency_parser.parse(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), mimetype='text/xml')


        @self.route('/unauthorized/<lang>/tag_lemmatise_depparse', methods=['GET', 'POST'])
        def unauthorized_tag_lemmatise_depparse(lang):
            '''

            @param lang:
            @type lang: string
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request)
            dependency_parser = dc['dependency_parser.' + lang]

            result = dependency_parser.parse(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), mimetype='text/xml')

        @self.route('/weblicht/<lang>/tag_lemmatise_depparse', methods=['GET', 'POST'])
        def weblicht_tag_lemmatise_depparse(lang):
            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            dependency_parser = dc['dependency_parser.' + lang]
            result = dependency_parser.parse(text)
            return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), mimetype='text/xml')


        @self.route('/login', methods=['POST'])
        def login():
            '''

            @return:
            @rtype: string
            '''
            username = request.form.get('username')
            password = request.form.get('password')

            if username is None or password is None:
                raise Unauthorized("Invalid username or password")
            user = UserModel.getByUsername(username)
            if user is None:
                raise Unauthorized("Invalid username or password")
            else:
                try:
                    token = user.generateToken(password)
                    token.save()
                    return jsonify(token.token, ensure_ascii=False)
                except ValueError as e:
                    raise Unauthorized(e.__str__())
