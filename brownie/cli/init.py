#!/usr/bin/python3

from docopt import docopt

from brownie import project
from brownie.cli.utils import notify


__doc__ = """Usage: brownie init [<path>] [options]

Arguments:
  <path>                Path to initialize (default is the current path)

Options:
  --force -f            Allow init inside a project subfolder
  --help -h             Display this message

brownie init is used to create new brownie projects. It creates the default
structure for the brownie environment:

build/                  Compiled contracts and test data
contracts/              Contract source code
reports/                Report files for contract analysis
scripts/                Scripts for deployment and interaction
tests/                  Scripts for project testing
brownie-config.json     Project configuration file"""


def main():
    args = docopt(__doc__)
    path = project.new(args["<path>"] or ".", args["--force"])
    notify("SUCCESS", f"Brownie environment has been initiated at {path}")
