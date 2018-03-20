#!/usr/bin/env python
""" mann: Simple, customisable quick-reference for shell commands """

# pylint: disable-msg=E0401; (Undefined variable)

import os
import json
import click


CONFIG_FILE = os.path.expanduser("~/.mannrc")


@click.group()
def mann():
	pass


@mann.command()
@click.argument("program")
def get(program):
	""" Retrieve stored commands. """

	records = _load_records()

	if not records:
		print("No commands have been added yet! Add some with --add/-a.")
		return

	if program not in records:
		print("No commands saved for this program. Add some with --add/-a.")
		return

	print(records[program])


@mann.command()
@click.argument("program")
@click.argument("command")
@click.argument("text")
def add(program, command, text):
	""" Add a new record. """

	raise NotImplementedError()


@mann.command()
@click.argument("program")
@click.argument("command")
def remove(program, command):
	""" Remove an existing record. """

	raise NotImplementedError()


def _load_records():
	if not os.path.lexists(CONFIG_FILE):
		return None

	with open(CONFIG_FILE, "r") as cfg_file:
		return json.load(cfg_file)
