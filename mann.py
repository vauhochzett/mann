#!/usr/bin/env python
""" mann module """

# pylint: disable-msg=E0401; (Undefined variable)

import os
import json
import click


CONFIG_FILE = os.path.expanduser("~/.mannrc")
ADD_HINT = " Add with --add/-a."
NO_RECORDS_ERROR = "No commands have been added yet!"


@click.group()
def mann():
	""" mann: Simple, customisable quick-reference for shell commands """
	pass


@mann.command()
@click.argument("program")
def get(program):
	""" Retrieve stored commands. """

	records = _load_records()

	if not records:
		print(NO_RECORDS_ERROR + ADD_HINT)
		return

	if program not in records:
		print("No commands saved for this program." + ADD_HINT)
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


def _save_records(records):
	with open(CONFIG_FILE, "w") as cfg_file:
		json.dump(records, cfg_file)
