# -*- coding: utf-8 -*-
import requests

from src.helpers import generate_token

print requests.post('http://0.0.0.0:8084/api/v1/sl/tag_ner',
                    data={'format':'json',
                          'text': "France Prešeren nam je dejal: žive naj vsi narodi, ki hrepene dočakat dan. Da koder sonce hodi prepir iz sveta bo pregnan.",
                          'request-id':  generate_token()},
                    headers={"Authorization": "cd060c15467c4cacac35cbd6df081507"}).content

