# -*- coding: utf-8 -*-
import sys
import os
import re
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, thispath + '/../reldi')

from cleo import Command, InputArgument, InputOption
from lexicon import Lexicon

class QueryLexiconCommand(Command):

    name = 'lexicon:query'

    description = 'Imports a lexicon from a file into an sqlite database'

    arguments = [
        {
            'name': 'surface',
            'description': 'Surface form',
            'required': False
        },
    ]

    def __init__(self):
        super(QueryLexiconCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """

        lexicon = Lexicon()
        lexicon.query_entry('sample')
