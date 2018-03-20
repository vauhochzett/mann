#!/usr/bin/env python
""" mann: Simple, customisable quick-reference for shell commands """

# pylint: disable-msg=E0401; (Undefined variable)

import click


def add(context, _, name):
	raise NotImplementedError()
	context.exit()


def remove(context, _, name):
	raise NotImplementedError()
	context.exit()

@click.command()
@click.option("--add", "-a", callback=add)
@click.option("--remove", "-r", callback=remove)
@click.argument("name")
def main(name):
	raise NotImplementedError()
