from cleo import Command

from src.core.restorer import DiacriticRestorer
from src.core.segmenter import Segmenter

class DiacriticRestoreCommand(Command):
    name = 'diacritic_restorer:restore'

    description = 'Dependency parse the input text'

    arguments = [
        {
            'name': 'lang',
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
        super(DiacriticRestoreCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        lang = i.get_argument('lang')
        text = i.get_argument('text')

        segmenter = Segmenter(lang)
        restorer = DiacriticRestorer(lang, segmenter)
        print restorer.restore(text)
