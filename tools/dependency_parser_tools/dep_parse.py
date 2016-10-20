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

        segmenter = Segmenter('hr')
        tagger = Tagger('hr', segmenter)
        lemmatiser = Lematiser('hr', segmenter, tagger)
        text = i.get_argument('text')

        with DependencyParser('hr', lemmatiser) as parser:
            result = parser.parse(text)
            print result
            # print jsonTCF('hr', text, result, lemma_idx=1, tag_idx=2, depparse_idx=3)
