import argparse

from django.core.management import BaseCommand

from deploy_django.models import DeployProtocol


class Command(BaseCommand):
    help = 'Collect a deployment output'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=argparse.FileType('r', encoding='UTF-8')
        )

    def handle(self, *args, **options):
        print(self.help)
        f = options['output']
        logging_output = f.read()
        print(repr(logging_output))
        DeployProtocol.objects.create(
            logging_output=logging_output
        )
