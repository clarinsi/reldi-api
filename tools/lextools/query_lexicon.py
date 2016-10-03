# -*- coding: utf-8 -*-
import sys
import os

from cleo import Command, InputArgument, InputOption
from src.core.lexicon import Lexicon


class QueryLexiconCommand(Command):

    name = 'lexicon:query'

    description = 'Imports a lexicon from a file into an sqlite database'

    arguments = [
        {
            'name': 'lang',
            'description': 'Language',
            'required': True
        },
        {
            'name': 'surface',
            'description': 'Surface form',
            'required': False
        },
        {
            'name': 'lemma',
            'description': 'Lemma',
            'required': False
        },
        {
            'name': 'msd',
            'description': 'MSD',
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

        lang = i.get_argument('lang')
        surface = i.get_argument('surface')
        lemma = i.get_argument('lemma')
        msd = i.get_argument('msd')

        lexicon = Lexicon(lang)
        print lexicon.query_entry(surface, lemma, msd, 'pet').__str__()