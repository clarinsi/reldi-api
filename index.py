# -*- coding: utf-8 -*-

import marshal, types
import sys
import json
sys.path.insert(0, '/root/reldi/reldi')

from flask import Flask
from flask.ext.cors import CORS
from flask import request
from flask import make_response

from lexicon import Lexicon

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
CORS(app)

def isset(v):
	return v is not None and v.strip() != ''

def jsonify(data, ensure_ascii=True, status=200, indent=4, sort_keys=True):
	response = make_response(json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys))
	response.headers['Content-Type'] = 'application/json; charset=utf-8'
	response.headers['mimetype'] = 'application/json'
	response.status_code = status
	return response

@app.errorhandler(Exception)
def handle_invalid_usage(error):
   response = jsonify(error.message)
   response.status_code = 400
   return response


@app.route('/')
def hello_world():
    return 'Hello World!'

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
		raise ValueError('Please specify a surface form, lemma or msd')

	# if rhyming_function_bytecode is not None:
	# 	code = marshal.loads(rhyming_function_bytecode)
	# 	func = types.FunctionType(code, globals(), "some_func_name")

	# 	return jsonify(func(10, 10))

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

	
if __name__ == '__main__':
    app.run(debug=True, host='46.101.225.178', port=5000)

