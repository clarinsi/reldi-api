import httplib, urllib

def getServerConfig():
	return {
		'url': '46.101.225.178',
		'port': 5000
	}

class Lexicon:
	'Lexicon class'

	def __init__(self, language = None, conn = None):
		self.language = language
		config = getServerConfig()
		self.conn = httplib.HTTPConnection(config['url'], config['port'])	
	  
	def query_entiries(self, surface = None, lemma = None, msd = None, rhymes_with = None, no_of_syllables = None ):  
		if self.language is None:
			raise ValueError("Language not set")
		
		params = {}
		if surface is not None: 
			params['surface'] = surface 
		if lemma is not None:
			params['lemma'] = lema
		if msd is not None:
			params['msd'] = msd
		if rhymes_with is not None:
			params['rhymes_with'] = rhymes_with
		if no_of_syllables is not None:
			params['no_of_syllables'] =  no_of_syllables
		
		self.conn.request("GET", "/api/v1/"+format(self.language)+"/lexicon?" + urllib.urlencode(params))
		result = self.conn.getresponse()
		if result.status is 200:
			data_result = result.read()
			print data_result
		else :
			raise ValueError("Connection not available")
			
if __name__ == "__main__":
	lex = Lexicon('hr')
	print lex.query_entiries('opor')