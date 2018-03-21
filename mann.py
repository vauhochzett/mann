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
@click.argument("program", default="all")
def get(program):
	""" Retrieve stored commands. """

	records = _load_records()

	if not records:
		print(NO_RECORDS_ERROR + ADD_HINT)
		return

	if program == "all":
		for key in records:
			_print_entries(key, records[key])
		return

	if program not in records:
		print("No commands saved for this program." + ADD_HINT)
		return

	_print_entries(program, records[program])


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

	conflicting_entries = [(c, t) for (c, t) in records[program]
		if c.startswith(command) or command.startswith(c)]
	if conflicting_entries:
		print("Ambiguous option! Conflicts with:")
		_print_entries(program, conflicting_entries)
		return

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
		_print_entries(program, to_delete)
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


### Pretty printing ###


def _print_entries(program, entries):
	min_width = 10
	longest_command = max([min_width] + [len(s) for (s, _) in entries])
	for entry in entries:
		print("   %s %s | %s" % (program, entry[0].ljust(longest_command), entry[1]))


### Record loading and saving ###


def _load_records():
	if not os.path.lexists(CONFIG_FILE):
		return None

	with open(CONFIG_FILE, "r") as cfg_file:
		return json.load(cfg_file)


def _save_records(records):
	with open(CONFIG_FILE, "w") as cfg_file:
		json.dump(records, cfg_file)
