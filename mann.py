#!/usr/bin/env python
""" mann module """

# pylint: disable-msg=E0401; (Undefined variable)

import argparse
import json
import os
import sys


CONFIG_FILE = os.path.expanduser("~/.mannrc")
ADD_HINT = " Add with 'add'"
NO_RECORDS_ERROR = "No commands have been added yet!"


def mann():
	""" mann: Simple, customisable quick-reference for shell commands """

	# argparse override to allow using "mann <program>"
	if len(sys.argv) == 2:
		if sys.argv[1].startswith("-") or sys.argv[1] in ["add", "remove"]:
			pass
		elif sys.argv[1] == "get":
			sys.argv.append("all")
		else:
			sys.argv.insert(1, "get")

	parser = argparse.ArgumentParser(prog="mann", description="Short-hand: 'mann <program>'")
	parser.add_argument("--version", "-v", action="version", version="%(prog)s 0.6.3")

	sub_commands = parser.add_subparsers()

	get_parser = sub_commands.add_parser("get", help="Retrieve stored commands")
	get_parser.add_argument("program")
	get_parser.set_defaults(function=get)

	add_parser = sub_commands.add_parser("add", help="Add a new record")
	add_parser.add_argument("program")
	add_parser.add_argument("command")
	add_parser.add_argument("text")
	add_parser.set_defaults(function=add)

	remove_parser = sub_commands.add_parser("remove", help="Remove an existing record.")
	remove_parser.add_argument("program")
	remove_parser.add_argument("command")
	remove_parser.set_defaults(function=remove)

	args = parser.parse_args()

	# For lack of the "required" argument in add_subparsers()
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit()

	args.function(args)


def get(args):
	""" Retrieve stored commands. """

	program = args.program

	records = _load_records()

	if not records:
		print(NO_RECORDS_ERROR + ADD_HINT)
		return

	if program == "all":
		for index, key in enumerate(sorted(records.keys())):
			_print_entries(key, records[key])

			if index < len(records) - 1:
				print("")
		return

	if program not in records:
		print("No commands saved for this program." + ADD_HINT)
		return

	_print_entries(program, records[program])


def add(args):
	""" Add a new record. """

	program = args.program
	command = args.command
	text = args.text

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


def remove(args):
	""" Remove an existing record. """

	program = args.program
	command = args.command

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
		json.dump(records, cfg_file, indent="\t")


if __name__ == "__main__":
	try:
		mann()
	except KeyboardInterrupt:
		# Exit code for Ctrl-C
		sys.exit(130)
