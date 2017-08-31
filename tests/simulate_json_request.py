# -*- coding: utf-8 -*-
import requests

from src.helpers import generate_token

print requests.post('http://0.0.0.0:8084/api/v1/sl/tag_ner',
                    data={'format':'json',
                          'text': "France Prešeren nam je dejal: žive naj vsi narodi, ki hrepene dočakat dan. Da koder sonce hodi prepir iz sveta bo pregnan.",
                          'request-id':  generate_token()},
                    headers={"Authorization": "9bf6d5452e1746d9b8eb6c5fbc9e52ed"}).content

