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
import zipfile
from HTMLParser import HTMLParser

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

        def authenticate_weblicht(api_method):
            @wraps(api_method)
            def verify(*args, **kwargs):
                validIp = \
                    request.remote_addr == '193.2.4.206' or \
                    request.remote_addr == '130.183.206.38' or \
                    request.remote_addr.startswith('134.2.128.') or \
                    request.remote_addr.startswith('134.2.129.')

                if not validIp:
                    raise Unauthorized('You are not allowed to make requests from this IP address')

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

                is_archive = True \
                    if 'file' in request.files \
                       and request.files['file'].mimetype in ["application/zip", "application/x-zip",
                                                              "application/x-zip-compressed",
                                                              "application/octet-stream",
                                                              "application/x-compress",
                                                              "application/x-compressed", "multipart/x-zip"]\
                    else False

                if is_archive:
                    zip_archive_filename = os.path.join(self.config['UPLOAD_FOLDER'],
                                                        get_filename_request_id(request.files['file'].filename))
                    request.files['file'].save(zip_archive_filename)
                    zip_archive = zipfile.ZipFile(zip_archive_filename)

                    files_to_process = [name for name in sorted(zip_archive.namelist())
                                        if "__MACOSX" not in name and not is_dir(name)]
                    for file_to_process in files_to_process:
                        with zip_archive.open(file_to_process, 'r') as f:
                            kwargs['file_'] = f
                            result = api_method(*args, **kwargs)
                            process_result(result, file_to_process)

                    zip_archive.close()
                    delete_file(zip_archive_filename)
                    create_zipfile(files_to_process)

                    return '{"filetype":"zip", "tokens":{"token":[]}}'

                else:
                    result = api_method(*args, **kwargs)
                    return process_result(result)

            return post_request

        def process_result(result, filename=None):
            if filename:
                filePath = os.path.join(self.config['UPLOAD_FOLDER'], get_filename_request_id(filename))
            else:
                filePath = os.path.join(self.config['UPLOAD_FOLDER'], get_request_id(request))

            raw = result.get_data()
            try:
                data = json.loads(raw)
                csvResult = []
                posTags = {}
                lemmas = {}
                tokens = {}
                parse = {}
                namedEntities = {}

                if 'POStags' in data:
                    for tag in data['POStags']['tag']:
                        posTags[tag['tokenIDs']] = tag

                if 'lemmas' in data:
                    for lemma in data['lemmas']['lemma']:
                        lemmas[lemma['tokenIDs']] = lemma

                if 'tokens' in data:
                    for token in data['tokens']['token']:
                        tokens[token['ID']] = token

                if 'namedEntities' in data:
                    for entity in data['namedEntities']['entity']:
                        namedEntities[entity['tokenIDs']] = entity

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
                        if tid in namedEntities:
                            csvResult[-1].append(namedEntities[tid]['value'])

                        csvResult[-1].append(token['start'])
                        csvResult[-1].append(token['end'])

                    csvResult.append([])

                with open(filePath, 'w') as f:
                    w = csv.writer(f, delimiter="\t")
                    w.writerows(csvResult)

            except Exception, e:
                print str(e)
                with open(filePath, 'w') as f:
                    f.write(raw)

            return result

        def is_dir(filename):
            if filename.endswith('/'):
                full_path = os.path.join(self.config['UPLOAD_FOLDER'], filename)
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
                return True
            return False

        def delete_file(filename):
            if os.path.exists(filename):
                os.remove(filename)

        def get_filename_request_id(filename):
            name, extension = os.path.splitext(filename)
            return name + "-" + get_request_id(request) + extension

        def create_zipfile(files):
            zip_filename = os.path.join(self.config['UPLOAD_FOLDER'], get_request_id(request) + ".zip")
            zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
            for f in files:
                filename = get_filename_request_id(f)
                filepath = os.path.join(self.config['UPLOAD_FOLDER'], filename)
                zipf.write(filepath, filename)
                delete_file(filepath)
            zipf.close()

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

        def weblicht_get_lang(request):
            with open('assets/tcfschema/d-spin-local_0_4.rng', 'r') as f:
                text = request.data
                relaxng_doc = etree.parse(f)
                relaxng = etree.RelaxNG(relaxng_doc)
                inputXml = re.sub(">\\s*<", "><", text)
                inputXml = re.sub("^\\s*<", "<", inputXml)

                doc = etree.parse(StringIO(inputXml))
                try:
                    relaxng.assertValid(doc)
                    h = HTMLParser()
                    attributes=doc.getroot()[1].attrib
                    if 'lang' in attributes:
                        return h.unescape(attributes['lang'])
                    else:
                        raise InvalidUsage('Please specify a lang parameter')
                except Exception as e:
                    raise InvalidUsage(e.message)

        def weblicht_get_text(request):
            with open('assets/tcfschema/d-spin-local_0_4.rng', 'r') as f:
                relaxng_doc = etree.parse(f)
                relaxng = etree.RelaxNG(relaxng_doc)

                text = request.data
                inputXml = re.sub(">\\s*<", "><", text)
                inputXml = re.sub("^\\s*<", "<", inputXml)
                doc = etree.parse(StringIO(inputXml))
                try:
                    relaxng.assertValid(doc)
                    h = HTMLParser()
                    return h.unescape(doc.getroot()[1][0].text)
                except Exception as e:
                    raise InvalidUsage(e.message)

        def get_text(format, request, file_=None):
            '''

            @param format:
            @type format: string
            @param request:
            @type request: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            params = request.form if request.method == 'POST' else request.args
            files = request.files
            if format == 'json':
                if file_:
                    return file_.read()
                elif 'file' in files:
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
        def segment(lang, file_=None):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            segmenter = dc['segmenter.' + lang]

            # Format properly
            result = map(lambda x: map(lambda y: (y,), x), segmenter.segment(text))

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result), mimetype='text/xml')


        @self.route('/<lang>/restore', methods=['GET', 'POST'])
        @authenticate
        def restore(lang, file_):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            restorer = dc['restorer.' + lang]
            result = restorer.restore(text)
            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, correction_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, correction_idx=1), mimetype='text/xml')


        @self.route('/<lang>/tag', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag(lang, file_=None):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''

            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            tagger = dc['tagger.' + lang]
            try:
                result = tagger.tag(text)

            except UnicodeDecodeError:
                text = ""
                result = ""

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, tag_idx=1), mimetype='text/xml')


        @self.route('/weblicht/tag', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_tag():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            tagger = dc['tagger.' + lang]
            result = tagger.tag(text)

            return Response(TCF(lang, text, result, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/lemmatise', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def lemmatise(lang, file_=None):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            lemmatiser = dc['lemmatiser.' + lang]
            try:
                result = lemmatiser.lemmatise(text)
            except UnicodeDecodeError:
                text = ""
                result = ""

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=1), mimetype='text/xml')


        @self.route('/weblicht/lemmatise', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_lemmatise():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            lemmatiser = dc['lemmatiser.' + lang]
            result = lemmatiser.lemmatise(text)

            return Response(TCF(lang, text, result, lemma_idx=1), mimetype='text/tcf+xml')

        @self.route('/<lang>/tag_lemmatise', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag_lematise(lang, file_=None):
            '''

            @return:
            @rtype:
            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            lemmatiser = dc['lemmatiser.' + lang]
            try:
                result = lemmatiser.tagLemmatise(text)
            except UnicodeDecodeError:
                text = ""
                result = ""

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')


        @self.route('/weblicht/tag_lemmatise', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_tag_lemmatise():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            lemmatiser = dc['lemmatiser.' + lang]
            result = lemmatiser.tagLemmatise(text)

            return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1), mimetype='text/xml')

        @self.route('/<lang>/tag_lemmatise_depparse', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag_lemmatise_depparse(lang, file_=None):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''
            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            dependency_parser = dc['dependency_parser.' + lang]
            try:
                result = dependency_parser.parse(text)
            except UnicodeDecodeError:
                text = ""
                result = ""

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), mimetype='text/xml')


        @self.route('/weblicht/tag_lemmatise_depparse', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_tag_lemmatise_depparse():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)
            dependency_parser = dc['dependency_parser.' + lang]
            result = dependency_parser.parse(text)

            return Response(TCF(lang, text, result, lemma_idx=2, tag_idx=1, depparse_idx=3), mimetype='text/xml')

        @self.route('/<lang>/tag_lemmatise_ner', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def tag_lemmatise_ner(lang, file_=None):
            '''

            @param lang:
            @type lang: string
            @param file_:
            @type file_: file
            @return:
            @rtype: string
            '''

            format = get_format(request)
            if not isset(format):
                raise InvalidUsage('Please specify a format')

            text = get_text(format, request, file_)
            # tagger = dc['tagger.' + lang]
            tagger = dc['ner_tagger.' + lang]

            try:
                result = tagger.tag(text)
            except UnicodeDecodeError:
                result = ""
                text = ""

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result, tag_idx=1,lemma_idx=2,ner_tag_idx=3), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result, tag_idx=1,lemma_idx=2,ner_tag_idx=3), mimetype='text/xml')

        @self.route('/weblicht/tag_lemmatise_ner', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_tag_lemmatise_ner():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)

            tagger = dc['ner_tagger.' + lang]
            result = tagger.tag(text)

            return Response(TCF(lang, text, result, tag_idx=1,ner_tag_idx=2), mimetype='text/xml')

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


        @self.route('/<lang>/normalise_with_csmtiser', methods=['GET', 'POST'])
        @authenticate
        @save_file
        def normalise_with_csmtiser(lang):
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
            # tagger = dc['tagger.' + lang]
            csmtiser = dc['csmtiser.' + lang]

            result = csmtiser.tag(text)

            if format == 'json':
                return jsonify(jsonTCF(lang, text, result), ensure_ascii=False)
            elif format == 'tcf':
                return Response(TCF(lang, text, result), mimetype='text/xml')

        @self.route('/weblicht/normalise_with_csmtiser', methods=['GET', 'POST'])
        @authenticate_weblicht
        def weblicht_normalise_with_csmtiser():
            lang = weblicht_get_lang(request)

            if request.headers['Content-Type'] != 'text/tcf+xml':
                raise BadRequest('Invalid content type: ' + request.headers['Content-Type'])

            request.get_data()
            text = weblicht_get_text(request)

            csmtiser = dc['csmtiser.' + lang]
            result = csmtiser.tag(text)

            return Response(TCF(lang, text, result), mimetype='text/xml')

            # tree = etree.fromstring(request.data)
            #
            # tokens = [i.text for i in tree[1][1]]
            # csmtiser = dc['csmtiser.' + lang]
            # token_to_normalized_token = csmtiser.normalise_tokens(tokens)
            #
            # for i in tree[1][1]:
            #     i.text = token_to_normalized_token[i.text]
            #
            # final_text = etree.tostring(tree, pretty_print=True, encoding='UTF-8').decode('utf-8')
            #
            # return Response(final_text, mimetype='text/xml')