from cleo import Command
from src.core.segmenter import Segmenter
from src.core.tagger import Tagger
from src.core.lematiser import Lematiser
from src.core.dependency_parser import DependencyParser
from src.helpers import jsonTCF


class DependecyParseCommand(Command):
    name = 'depparse:parse'

    description = 'Dependency parse the input text'

    arguments = [
        {
            'name': 'language',
            'description': 'Language',
            'required': True
        },
        {
            'name': 'text',
            'description': 'The text to be parsed',
            'required': True
        }
    ]

    def __init__(self):
        super(DependecyParseCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        language = i.get_argument('language')
        text = i.get_argument('text')

        segmenter = Segmenter(language)
        tagger = Tagger(language, segmenter)
        lemmatiser = Lematiser(language, segmenter, tagger)

        parser = DependencyParser(language, lemmatiser)
        result = parser.parse(text)
        print result
            # print jsonTCF('hr', text, result, lemma_idx=1, tag_idx=2, depparse_idx=3)
