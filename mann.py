#!/usr/bin/env python
""" mann: Simple, customisable quick-reference for shell commands """

# pylint: disable-msg=E0401; (Undefined variable)

import click

@click.command()
@click.option("--add", "-a", 'mode', flag_value="add")
@click.option("--remove", "-r", 'mode', flag_value="remove")
@click.argument("name")
def main(mode, name):
	if mode == "add":
		add(name)
	elif mode == "remove":
		remove(name)

	raise NotImplementedError()


def add(name):
	raise NotImplementedError()
	exit()


def remove(name):
	raise NotImplementedError()
	exit()
