import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout


class Deployment:
    def __init__(self):
        assert 'DJANGO_SETTINGS_MODULE' in os.environ

        with tempfile.NamedTemporaryFile(mode='w') as f:
            with redirect_stdout(f), redirect_stderr(f):
                print('Stat deploy hook')
                self.deploy_hook()
                print('Deploy hook ended')
            self.submit_deploy_protocol(f)

    def deploy_hook(self):
        raise NotImplemented

    def submit_deploy_protocol(self, f):
        print('submit deploy protocol')
        f.flush()

        from django.core.management import execute_from_command_line
        args = [sys.argv[0]]
        args += ['deploy_results', '--output', f.name]
        print(f'call: {args}')
        execute_from_command_line(args)

        # import django
        # from django.core import management
        # django.setup()
        #
        # management.call_command(
        #     deploy_results.Command(),
        #     output='test!'
        # )
