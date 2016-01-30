# -*- coding: utf-8 -*-
import sys
import os
import regex
import codecs

dbpath = os.path.realpath('../db')
sys.path.append(dbpath)

from cleo import Command, InputArgument, InputOption
from lexicon_db import LexiconDB

class ImportLexiconCommand(Command):

    name = 'lexicon:import'

    description = 'Imports a lexicon from a file into an sqlite database'

    arguments = [
        {
            'name': 'path',
            'description': 'Path to the lexicon',
            'required': True
        },
        {
            'name': 'lang',
            'description': 'Lexicon language',
            'required': True
        }
    ]

    def __init__(self):
        super(ImportLexiconCommand, self).__init__()
        # Instantiate db connection
        self.lineDelimiter = regex.compile("[^\t]+")

    def createTable(self):
        statement = """
            CREATE TABLE IF NOT EXISTS lexicon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surface TEXT,
                lemma TEXT,
                tags TEXT,
                no_of_syllables INTEGER,
                last_syllable TEXT
            );
            CREATE INDEX lemma_idx ON lexicon (lemma);
            CREATE INDEX surface_idx ON lexicon (surface);
            CREATE INDEX tags_idx ON lexicon (tags);
            CREATE INDEX tags_idx ON lexicon (lemma, surface, tags);
        """

        self.db.command(statement)

    def insertLexiconEntry(self, line):
        tokens = line.split("\t")
        (surface, lemma, tags) = (tokens[0], tokens[1], tokens[2])

        #  -- vocals or syllable-forming-r-s (surrounded with non-vocals or start / end of string)
        # Use regex library which supports variable length look-behind / look-ahead
        r_syl = regex.compile('[aeiou]|((?<=^|[^aeiou])r(?=$|[^aeiou]))')
        syllables = [(m.start(0), m.end(0)) for m in r_syl.finditer(surface)]
        if len(syllables) == 0:
            last_syllable = surface
        else: 
            idxs = syllables[-1]
            idx_from = idxs[0] - 1
            idx_to = idxs[1] + 1
            last_syllable = surface[idx_from:idx_to]

        no_syl = len(r_syl.findall(surface)) + 1;
        # Insert row into database
        sql = "INSERT INTO lexicon (surface, lemma, tags, no_of_syllables, last_syllable) VALUES (?, ?, ?, ?, ?)"
        self.db.command(sql, (surface, lemma, tags, no_syl, last_syllable.encode('utf-8')))

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        path = i.get_argument('path')
        language = i.get_argument('lang')

        # Initialize database
        self.db = LexiconDB(language);

        # Create table
        self.createTable();
        count = 0
        # Read lexicon and import lines
        with codecs.open(path, 'r', encoding='utf-8') as lexfile:
            for line in lexfile:
                self.insertLexiconEntry(line.rstrip())
                # count += 1
                # if count == 100:
                #     break
