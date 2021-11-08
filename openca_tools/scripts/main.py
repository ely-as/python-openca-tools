import argparse
from pathlib import Path
from typing import List, Optional

from openca_tools.csvify import create


def cmd() -> None:
    Command().execute()


class Command(object):
    command: str = ''
    title: str = 'openca-tools'
    description: str = (
        'Tools for processing Open Government Canada (open.canada.ca) '
        'datasets.'
    )
    help: str = 'Valid subcommands.'

    def __init__(
        self, parser: Optional[argparse.ArgumentParser] = None
    ) -> None:
        super().__init__()
        if parser is None:
            parser = argparse.ArgumentParser()
        self.parser = parser
        self.add_arguments()
        parser.set_defaults(func=self._exec_handle)
        self.subcommands = []
        subclasses = self._get_subclasses()
        if subclasses:
            kwargs = {k: getattr(self, k) for k in
                      ['title', 'description', 'help'] if getattr(self, k)}
            self.subparsers = parser.add_subparsers(**kwargs)
            for subclass in subclasses:
                subparser = self.subparsers.add_parser(subclass.command)
                self.subcommands.append(subclass(subparser))

    def _get_subclasses(self) -> List:
        """Get direct subclasses of this class."""
        return self.__class__.__subclasses__()

    def add_arguments(self) -> None:
        pass

    def execute(self) -> None:
        args = self.parser.parse_args()
        options = vars(args)
        pos_args = options.pop('args', ())
        args.func(*pos_args, **options)

    def _exec_handle(self, *args, **options) -> None:
        self.args = args
        self.options = options
        self.handle(*args, **options)

    def handle(self, *args, **options) -> None:
        self.parser.print_help()


class CollectionCommand(Command):
    command = 'csvify'

    def add_arguments(self) -> None:
        self.parser.add_argument(
            dest='fp',
            help="An SDMX .xml file that starts with 'Generic_'.",
            default=None
        )

    def handle(self, *args, **options) -> None:
        create(Path(options['fp']))
