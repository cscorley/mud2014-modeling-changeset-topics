from __future__ import print_function

import click

class Config:
    def __init__(self):
        self.verbose = False
        # set all possible config options here


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    """
    Topic of Change
    """
    # Only set config items here, this function is unused otherwise.
    config.verbose = verbose


@cli.command()
#@click.option('--repeat', default=1,
#        help='How many times to greet the thing.')
@click.argument('project')
@pass_config
def corpora(config, project):
    """
    Builds the basic corpora for a project
    """
    if config.verbose:
        print('We are in verbose mode.')

    print('Creating corpus for: %s' % project)


@cli.command()
@click.argument('project')
@pass_config
def preprocess(config, project):
    """
    Runs the preprocessing steps on a corpus
    """
    print('Preproccessing corpus for: %s' % project)


@cli.command()
@click.argument('project')
@pass_config
def model(config, project):
    """
    Builds a model for the corpora
    """
    print('Building topic models for: %s' % project)


@cli.command()
@click.argument('project')
@pass_config
def evaluate(config, project):
    """
    Evalutates the models
    """
    print('Evalutating models for: %s' % project)


@cli.command()
@click.argument('project')
@pass_config
@click.pass_context
def run_all(context, config, project):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    print('Doing everything for: %s' % project)
    context.forward(corpora)
    context.forward(preprocess)
    context.forward(model)
    context.forward(evaluate)
