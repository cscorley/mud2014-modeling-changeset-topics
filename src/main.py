#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import print_function

import csv
import sys
from collections import namedtuple

import click
import gittle
import dulwich

class Config:
    def __init__(self):
        self.verbose = False
        self.base_path = '.'
        self.project = None
        self.repo = None
        # set all possible config options here

def error(msg, errorno=1)
    print(msg, file=sys.stderr)
    sys.exit(errorno)


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--base_path', default='/var/opt/topic-of-change/',
        help="Set the directory to work within")
@click.argument('project')
@pass_config
def main(config, verbose, base_path, project):
    """
    Topic of Change
    """

    # Only set config items here, this function is unused otherwise.
    config.verbose = verbose
    config.base_path = base_path
    with open("projects.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        Project = namedtuple('Project',  ' '.join(header))

        # figure out which column index contains the project name
        name_idx = header.index("short_name")

        # find the project in the csv, adding it's info to config
        for row in reader:
            if project == row[name_idx]:
                # 🎶  do you believe in magicccccc
                # in a young girl's heart? 🎶
                config.project = Project(*row)
                break

        # we can access project info by:
        #    config.project.url => "http://..."
        #    config.project.name => "Blah Name"

        if config.project is None:
            error("Could not find the project '%s' in 'projects.csv'!" % project)

@main.command()
@pass_config
@click.pass_context
def clone(context, config):
    """
    Clones the project repository
    """
    print('Cloning repo for: %s' % config.project.name)

    tries = 10
    while config.repo is None and tries > 0:
        tries -= 1
        try:
            config.repo = open_or_clone(config.base_path, config.project)
        except dulwich.errors.GitProtocolError as e:
            config.repo = None

    if config.repo is None
        error('Could not clone repository within 10 tries :(')

def open_or_clone(path, project):
    full_path = path + '/' + project.short_name
    try:
        return gittle.Gittle(full_path)
    except dulwich.errors.NotGitRepository:
        return gittle.Gittle.clone_bare(project.url, full_path)


@main.command()
@pass_config
@click.pass_context
def corpora(context, config):
    """
    Builds the basic corpora for a project
    """

    if config.repo is None:
        # clone repo
        context.forward(clone)

    print('Creating corpus for: %s' % config.project.name)


@main.command()
@pass_config
@click.pass_context
def preprocess(context, config):
    """
    Runs the preprocessing steps on a corpus
    """
    print('Preproccessing corpus for: %s' % config.project.name)


@main.command()
@pass_config
@click.pass_context
def model(context, config):
    """
    Builds a model for the corpora
    """
    print('Building topic models for: %s' % config.project.name)


@main.command()
@pass_config
@click.pass_context
def evaluate(context, config):
    """
    Evalutates the models
    """
    print('Evalutating models for: %s' % config.project.name)


@main.command()
@pass_config
@click.pass_context
def run_all(context, config):
    """
    Runs corpora, preprocess, model, and evaluate in one shot.
    """
    print('Doing everything for: %s' % config.project.name)
    context.forward(clone)
    context.forward(corpora)
    context.forward(preprocess)
    context.forward(model)
    context.forward(evaluate)