import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Start a deployment'

    def handle(self, *args, **options):
        script = Path(settings.DEPLOYMENT_SCRIPT)
        assert script.is_file(), f'File not found: {script}'
        assert os.access(script, os.X_OK), f'File not executeable: {script}'

        print(f'Start deploy script: {script}...')
        p = subprocess.run(
            script
        )
        print(p)
        print('Deploy script end')
