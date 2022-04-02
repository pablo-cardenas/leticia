import json
import click
from . import run


@click.group()
def cli():
    pass


@cli.command('run')
@click.argument('ncol', type=int)
@click.argument('nrow', type=int)
@click.argument('params')
@click.argument('seed', type=int)
@click.argument('output', type=click.Path(exists=False))
def run_command(ncol, nrow, params, seed, output):
    result = run(ncol, nrow, json.loads(params), seed)
    with open(output, 'w') as f:
        f.write(json.dumps(result).replace('Infinity', 'null'))
