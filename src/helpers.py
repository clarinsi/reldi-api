import json
from flask import make_response
from lxml import etree
from StringIO import StringIO
import hashlib, uuid
from datetime import datetime, timedelta
import pytz


def generate_token():
    return uuid.uuid4().hex


def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return salt + ':' + hashed_password


def verify_password(password, hash):
    salt, hashed_password = hash.split(':')
    return hashed_password == hashlib.sha512(password + salt).hexdigest()


def to_unix_timestamp(dt):
    if dt is None:
        return None

    tz = pytz.timezone('UTC')
    dt_with_tz = tz.localize(dt, is_dst=None)
    ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return ts


def empty(v):
    return v == ''


def isset(v):
    return v is not None and v.strip() != ''


def jsonify(data, ensure_ascii=False, status=200, indent=4, sort_keys=True):
    response = make_response(json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


def jsonResponse(query, data):
    return jsonify({
        'query': query,
        'success': True,
        'result': data,
        'count': len(data)
    }, ensure_ascii=False)


def jsonTCF(lang, text, result, lemma_idx=None, tag_idx=None, output_sentences=True):
    output = {}
    output['text'] = text
    output['tokens'] = []
    output['sentences'] = []
    output['lemmas'] = []
    output['POSTags'] = []

    token_id = 0
    for s_idx, sentence in enumerate(result):
        token_ids = []
        output['sentences'].append([])
        if lemma_idx is not None:
            output['lemmas'].append([])
        if tag_idx is not None:
            output['POSTags'].append([])

        for token in sentence:
            output['tokens'].append({
                'ID': "t_" + str(token_id),
                'startChar': str(token[0][1]),
                'endChar': str(token[0][2]),
                'value': token[0][0]
            })
            token_ids.append("t_" + str(token_id))
            if lemma_idx is not None:
                output['lemmas'][-1].append({
                    'ID': 'le_' + str(token_id),
                    'tokenIDs': 't_' + str(token_id),
                    'value': token[lemma_idx]
                })

            if tag_idx is not None:
                output['POSTags'][-1].append({
                    'ID': 'pt_' + str(token_id),
                    'tokenIDs': 't_' + str(token_id),
                    'value': token[tag_idx]
                })

            token_id += 1

        output['sentences'][-1].append({
            'ID': 's_' + str(s_idx),
            'tokenIDs': " ".join(token_ids)
        })

        # sentence_output += "\t<sentence ID=\"ID=s_{0}\" tokenIDs=\"{1}\">".format(s_idx, " ".join(token_ids))
        # sentence_output += "".join(map(lambda x: x[0], sentence)) + "</sentence>\n"

    if len(output['POSTags']) == 0:
        del output['POSTags']

    if len(output['lemmas']) == 0:
        del output['lemmas']

    return output


def TCF(lang, text, result, lemma_idx=None, tag_idx=None, output_sentences=True):
    output = ''
    sentence_output = ''
    token_output = ''
    tags_output = ''
    lemmas_output = ''

    token_id = 0
    for s_idx, sentence in enumerate(result):
        token_ids = []
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

            token_id += 1

        sentence_output += "<sentence ID=\"s_{0}\" tokenIDs=\"{1}\" />".format(s_idx, " ".join(token_ids))

    output += "<tokens>" + token_output + "</tokens>"
    if output_sentences:
        output += "<sentences>" + sentence_output + "</sentences>"
    if not empty(lemmas_output):
        output += "<lemmas>" + lemmas_output + "</lemmas>"
    if not empty(tags_output):
        output += "<POStags tagset=\"mte-hr-v4r\">" + tags_output + "</POStags>"

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
