#!/usr/bin/env python
""" mann module """

# pylint: disable-msg=E0401; (Undefined variable)

import os
import json
import click


CONFIG_FILE = os.path.expanduser("~/.mannrc")
ADD_HINT = " Add with 'add'"
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

	records = _load_records()

	if not records:
		records = {}

	if program not in records:
		records[program] = []

	records[program].append((command, text))
	records[program].sort(key=lambda tup: tup[0])

	_save_records(records)


@mann.command()
@click.argument("program")
@click.argument("command")
def remove(program, command):
	""" Remove an existing record. """

	records = _load_records()

	if not records:
		print(NO_RECORDS_ERROR)
		return

	to_delete = [(x, y) for (x, y) in records[program] if x.startswith(command)]
	if (program not in records
		or not to_delete):
		print("No such record found!")
		return

	if len(to_delete) > 1:
		print("Ambiguous argument. Found the following entries:")
		print(to_delete)
		return

	for i in range(len(records[program])):
		cmd = records[program][i][0]
		if cmd.startswith(command):
			del(records[program][i])
			print("Okay.")
			break

	if not records[program]:
		records.pop(program)

	_save_records(records)


def _load_records():
	if not os.path.lexists(CONFIG_FILE):
		return None

	with open(CONFIG_FILE, "r") as cfg_file:
		return json.load(cfg_file)


def _save_records(records):
	with open(CONFIG_FILE, "w") as cfg_file:
		json.dump(records, cfg_file)
