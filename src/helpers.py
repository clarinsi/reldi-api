import json
from flask import make_response
from lxml import etree
from StringIO import StringIO
import hashlib, uuid
from datetime import datetime, timedelta
import pytz


def generate_token():
    """
    Generates an authentication token
    """
    return uuid.uuid4().hex


def hash_password(password):
    """
    Returns the hash for a password
    """
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return salt + ':' + hashed_password


def verify_password(password, hash):
    """
    Verifies whether a hash matches the password
    """
    salt, hashed_password = hash.split(':')
    return hashed_password == hashlib.sha512(password + salt).hexdigest()


def to_unix_timestamp(dt):
    """
    Converts a datetime object into a unit timestamp object
    """
    if dt is None:
        return None

    tz = pytz.timezone('UTC')
    dt_with_tz = tz.localize(dt, is_dst=None)
    ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return ts


def empty(v):
    """
    Checks whether a string is empty
    """
    return v == ''


def isset(v):
    """
    Checkts whether a variable is not None and not empty
    """
    return v is not None and v.strip() != ''


def jsonify(data, ensure_ascii=False, status=200, indent=4, sort_keys=True):
    """
    Serializes an object into a HTTP json response
    """
    response = make_response(json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


def jsonResponse(query, data):
    """
    Transforms an object into a API json response
    """
    return jsonify({
        'query': query,
        'success': True,
        'result': data,
        'count': len(data)
    }, ensure_ascii=False)


def jsonTCF(lang, text, result, lemma_idx=None, tag_idx=None, correction_idx=None, depparse_idx = None, output_sentences=True):
    """
    Transforms an object into a API json response similar to the TCF format
    """
    output = {}
    output['text'] = text
    output['tokens'] = {
        'token': []
    }
    output['sentences'] = {
        'sentence': []
    }
    output['lemmas'] = {
        'lemma': []
    }
    output['POStags'] = {
        'tag': []
    }
    output['orthography'] = {
        'correction': []
    }
    output['depparsing'] = {
        'parse': []
    }

    previous_token_sum = 0
    token_id = 0
    for s_idx, sentence in enumerate(result):
        token_ids = []

        if depparse_idx is not None:
            output['depparsing']['parse'].append({
                'dependency': []
            })

        for t_idx, token in enumerate(sentence):

            output['tokens']['token'].append({
                'ID': "t_" + str(token_id),
                'startChar': str(token[0][1]),
                'endChar': str(token[0][2]),
                'text': token[0][0]
            })
            token_ids.append("t_" + str(token_id))
            if lemma_idx is not None:
                output['lemmas']['lemma'].append({
                    'ID': 'le_' + str(token_id),
                    'tokenIDs': 't_' + str(token_id),
                    'text': token[lemma_idx]
                })

            if tag_idx is not None:
                output['POStags']['tag'].append({
                    'ID': 'pt_' + str(token_id),
                    'tokenIDs': 't_' + str(token_id),
                    'text': token[tag_idx]
                })
            if correction_idx is not None:
                output['orthography']['correction'].append({
                    'ID': 'pt_' + str(token_id),
                    'tokenIDs': 't_' + str(token_id),
                    'text': token[correction_idx]
                })
            if depparse_idx is not None:
                govId = int(token[depparse_idx][0]) - 1 + previous_token_sum
                if int(govId) != previous_token_sum - 1:
                    output['depparsing']['parse'][s_idx]['dependency'].append({
                        'govIDs': "t_" + str(govId),
                        'depIDs': "t_" + str(token_id),
                        'func': token[depparse_idx][1]
                    })
                else:
                    output['depparsing']['parse'][s_idx]['dependency'].append({
                        'depIDs': "t_" + str(token_id),
                        'func': token[depparse_idx][1]
                    })

            token_id += 1

        output['sentences']['sentence'].append({
            'ID': 's_' + str(s_idx),
            'tokenIDs': " ".join(token_ids)
        })

        # sentence_output += "\t<sentence ID=\"ID=s_{0}\" tokenIDs=\"{1}\">".format(s_idx, " ".join(token_ids))
        # sentence_output += "".join(map(lambda x: x[0], sentence)) + "</sentence>\n"

    if len(output['POStags']['tag']) == 0:
        del output['POStags']

    if len(output['lemmas']['lemma']) == 0:
        del output['lemmas']

    if len(output['orthography']['correction']) == 0:
        del output['orthography']

    if len(output['depparsing']['parse']) == 0:
        del output['depparsing']

    return output


def TCF(lang, text, result, lemma_idx=None, tag_idx=None, correction_idx=None, depparse_idx=None, output_sentences=True):
    """
    Transforms an object into a TCF response
    """
    output = ''
    sentence_output = ''
    token_output = ''
    tags_output = ''
    lemmas_output = ''
    orthography_output = ''
    depparse_output = ''

    previous_token_sum = 0
    token_id = 0
    for s_idx, sentence in enumerate(result):
        token_ids = []
        parses = []
        for token in sentence:
            token_output += "<token ID=\"t_{0}\" startChar=\"{1}\" endChar=\"{2}\">{3}</token>".format(token_id,
                                                                                                           token[0][1],
                                                                                                           token[0][2],
                                                                                                           token[0][0])
            token_ids.append("t_" + str(token_id))

            if lemma_idx is not None:
                lemmas_output += "<lemma ID=\"le_{0}\" tokenIDs=\"t_{0}\">{1}</lemma>".format(token_id,
                                                                                                  token[lemma_idx])

            if tag_idx is not None:
                tags_output += "<tag ID=\"pt_{0}\" tokenIDs=\"t_{0}\">{1}</tag>".format(token_id, token[tag_idx])

            if correction_idx is not None:
                orthography_output += "<correction ID=\"pt_{0}\" tokenIDs=\"t_{0}\">{1}</correction>".format(token_id, token[correction_idx])

            if depparse_idx is not None:
                govId = int(token[depparse_idx][0]) - 1 + previous_token_sum
                if int(govId) != previous_token_sum - 1:
                    parses.append("<dependency govIDs=\"t_{0}\" depIDs=\"t_{1}\" func=\"{2}\" />".format(govId, token_id, token[depparse_idx][1]))
                else:
                    parses.append("<dependency depIDs=\"t_{0}\" func=\"{1}\" />".format(token_id, token[depparse_idx][1]))

            token_id += 1
        previous_token_sum += len(sentence)

        sentence_output += "<sentence ID=\"s_{0}\" tokenIDs=\"{1}\" />".format(s_idx, " ".join(token_ids))
        if depparse_idx is not None:
            depparse_output += "<parse ID=\"d_{0}\">".format(s_idx) + "".join(parses) + "</parse>"

    output += "<tokens>" + token_output + "</tokens>"
    if output_sentences:
        output += "<sentences>" + sentence_output + "</sentences>"
    if not empty(lemmas_output):
        output += "<lemmas>" + lemmas_output + "</lemmas>"
    if not empty(tags_output):
        output += "<POStags tagset=\"mte-hr-v5\">" + tags_output + "</POStags>"
    if not empty(orthography_output):
        output += "<orthography>" + orthography_output + "</orthography>"
    if not empty(depparse_output):
        output += "<depparsing tagset=\"UD-v1.3\" emptytoks=\"false\" multigovs=\"false\">" + depparse_output + "</depparsing>"


    output = """<?xml version="1.0" encoding="UTF-8"?>
    <D-Spin xmlns="http://www.dspin.de/data" version="0.4">
        <MetaData xmlns="http://www.dspin.de/data/metadata"/>
        <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="{0}">
            <text>{2}</text>
            {1}
        </TextCorpus>
    </D-Spin>""".format(lang, output, text)

    x = etree.parse(StringIO(output), etree.XMLParser(remove_blank_text=True))
    return etree.tostring(x.getroot(), pretty_print=True)
