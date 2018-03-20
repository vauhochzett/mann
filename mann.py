#!/usr/bin/env python
""" mann: Simple, customisable quick-reference for shell commands """

# pylint: disable-msg=E0401; (Undefined variable)

import os
import json
import click


CONFIG_FILE = os.path.expanduser("~/.mannrc")


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
	""" Retrieve records. """
	raise NotImplementedError()


def _load_records():
	if not os.path.lexists(CONFIG_FILE):
		return None

	with open(CONFIG_FILE, "r") as cfg_file:
		return json.load(cfg_file)
