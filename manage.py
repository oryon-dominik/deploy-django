#!/usr/bin/env python3
import os
import sys
from pathlib import Path


BASE_PATH = Path(__file__).parent


def main():
    assert 'DJANGO_SETTINGS_MODULE' in os.environ, 'No "DJANGO_SETTINGS_MODULE" in environment!'

    # Change to /src/ and add it to sys.path
    src_path = Path(BASE_PATH, 'src').resolve()
    assert src_path.is_dir(), f'Path not exists: {src_path}'
    sys.path.insert(0, str(src_path))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()