#!/usr/bin/env python3
# coding: utf-8

import typer
import subprocess
import platform
from pathlib import Path


app = typer.Typer()
USE_DOCKER = False
DEBUG = True  # print what commands get executed

def echo(
    message: str,
    fg_color: str = typer.colors.WHITE,
    bg_color: str = typer.colors.BLACK,
    bold: bool = False
    ):
    """colors:
        "bright_" + black, red, green, yellow, blue, magenta, cyan, white
    """
    typer.echo(
        typer.style(
            message,
            fg=fg_color,
            bg=bg_color,
            bold=bold,
        )
    )

def run_command(command, debug=False, cwd='./backend', env=None, managepy=False, docker=False):
    if managepy:
        command = f"python manage.py {command}"
    if docker:
        cwd = '.'
        command = f"docker-compose run django {command}"
    if debug:
        echo(f">>> Running command: {command}")
    try:
        subprocess.run(command, cwd=cwd, env=env)
    except FileNotFoundError:
        echo(f'The command {command} threw a FileNotFoundError', fg_color=typer.colors.RED)

def run_docker_compose_command(command, debug=False, cwd='.', env=None, docker=False):
    if not docker:
        echo(f">>> {command} requires a dockerized project")
        return
    if debug:
        echo(f">>> Running command: {command}")
    try:
        subprocess.run(command, cwd=cwd, env=env)
    except FileNotFoundError:
        echo(f'The command {command} threw a FileNotFoundError', fg_color=typer.colors.RED)

def delete_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            delete_folder(element)
        else:
            element.unlink()
    path.rmdir()

def clean_build():
    echo(f"Unlinking build-files: build/; dist/ *.egg-info; __pycache__;", fg_color=typer.colors.RED)
    cwd = Path('.')
    [delete_folder(p) for p in cwd.rglob('build')]
    [delete_folder(p) for p in cwd.rglob('dist')]
    [delete_folder(p) for p in cwd.rglob('*.egg-info')]
    [delete_folder(p) for p in cwd.rglob('__pycache__')]

def clean_pyc():
    echo(f"Unlinking caches: *.pyc; *pyo; *~;", fg_color=typer.colors.RED)
    [p.unlink() for p in Path('.').rglob('*.py[co]')]
    [p.unlink() for p in Path('.').rglob('*~')]

@app.command()
def clean():
    clean_build()
    clean_pyc()

@app.command()
def manage(command: str, second: str = typer.Argument(None)):
    if second:
        echo(f'Commands with arguments are not supported via this interface yet', fg_color=typer.colors.RED)
        return
    run_command(f'{command}', debug=DEBUG, managepy=True, docker=USE_DOCKER)

@app.command()
def compose(command: str, second: str = typer.Argument(None)):
    if second:
        echo(f'Commands with arguments are not supported via this interface yet', fg_color=typer.colors.RED)
        return
    run_docker_compose_command(f'{command}', debug=DEBUG, docker=USE_DOCKER)

@app.command()
def build(nocache: bool = False):
    command = "docker-compose build"
    if nocache:
        command = f"{command} --no-cache"
    run_docker_compose_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def up(orphans: bool = False):
    command = "docker-compose up"
    if orphans:
        command = f"{command} --remove-orphans"
    run_docker_compose_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def down():
    command = "docker-compose down"
    run_docker_compose_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def pytest(test_path: str = typer.Argument(None)):
    command = "pytest"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def test(test_path: str = typer.Argument(None)):
    pytest(test_path)

@app.command()
def black(path: str = typer.Argument(None)):
    command = "black"
    if path is not None:
        command = f"{command} {path}"
    run_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def coverage():
    commands = [
        "coverage run --source='.' manage.py test",
        "coverage report"
    ]
    for command in commands:
        run_command(command, debug=DEBUG, docker=USE_DOCKER)

@app.command()
def docs(doc_path: Path = Path('./backend/docs')):
    [p.unlink(missing_ok=True) for p in doc_path.rglob('*.rst') if not p.name == 'index.rst']
    run_command("sphinx-apidoc -o . .. --ext-autodoc", debug=DEBUG, cwd=doc_path)
    if not platform.system() == "Windows":
        run_command("make html", debug=DEBUG, cwd=doc_path)
        when = "now"
    else:
        echo(f"Make failed (Windows) run it manually with:\n{doc_path.resolve()}\make html", fg_color=typer.colors.RED)
        when = "then"
    file_url = f'file://{Path("docs/_build/html/index.html").resolve()}'
    echo(f"Docs are {when} available at: {file_url}", fg_color=typer.colors.BLACK, bg_color=typer.colors.WHITE)

@app.command()
def poetryinstall():
    run_command(f'poetry install', debug=DEBUG, managepy=True, docker=False)

@app.command()
def rebuild(nocache: bool = False):
    poetryinstall()
    build(nocache=nocache)
    initialize()

@app.command()
def makemigrations():
    run_command('makemigrations', debug=DEBUG, managepy=True, docker=USE_DOCKER)

@app.command()
def migrate():
    run_command('migrate', debug=DEBUG, managepy=True, docker=USE_DOCKER)

@app.command()
def resetschema():
    run_command('reset_schema --noinput', debug=DEBUG, managepy=True, docker=USE_DOCKER)

@app.command()
def deletemigrations(apps_path: Path = Path('.')):  # it's usally APPS_DIR 'apps/' !
    if not apps_path.exists():
        echo(f'Directory {apps_path.resolve()} does not exist', fg_color=typer.colors.RED)
        return

    app_dirs = [
        app_dir
        for app_dir in apps_path.iterdir()
        if app_dir.is_dir() and app_dir.name != "__pycache__"
    ]

    for d in app_dirs:
        migrations = Path(d) / "migrations"
        if migrations.exists():
            for f in [m for m in migrations.iterdir() if not m.is_dir()]:
                if not '__init__' in f.name:
                    echo(f"Deleting migration: {f.parent}/{f.name}", fg_color=typer.colors.RED)
                    f.unlink()

@app.command()
def initialize():
    echo(f'Reset the database schema...', fg_color=typer.colors.RED)
    resetschema()
    echo(f'Deleting migrations...', fg_color=typer.colors.RED)
    deletemigrations()
    echo(f'Makemigrations...', fg_color=typer.colors.GREEN)
    makemigrations()
    echo(f'Migrate...', fg_color=typer.colors.GREEN)
    migrate()
    echo(f'Creating pytest DB...', fg_color=typer.colors.GREEN)
    run_command("pytest --quiet --create-db", debug=DEBUG, docker=USE_DOCKER)
    echo(f'Successfully initialized the project...', fg_color=typer.colors.GREEN)

@app.command()
def init():
    initialize()

@app.command()
def mm():
    makemigrations()

@app.command()
def mig():
    migrate()

if __name__ == "__main__":
    app()
