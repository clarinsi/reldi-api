from cleo import Command
from src.core.segmenter import Segmenter


class SegmentCommand(Command):
    name = 'segmenter:segment'

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
        super(SegmentCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """

        segmenter = Segmenter('hr')
        text = i.get_argument('text')
        print segmenter.segment(text)
