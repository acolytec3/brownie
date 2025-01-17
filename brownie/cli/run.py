#!/usr/bin/python3

from docopt import docopt

from brownie import network, project, run
from brownie.test.output import print_gas_profile
from brownie._config import ARGV, CONFIG, update_argv_from_docopt


__doc__ = f"""Usage: brownie run <filename> [<function>] [options]

Arguments:
  <filename>              The name of the script to run
  [<function>]            The function to call (default is main)

Options:
  --network [name]        Use a specific network (default {CONFIG['network']['default']})
  --gas -g                Display gas profile for function calls
  --tb -t                 Show entire python traceback on exceptions
  --help -h               Display this message

Use run to execute scripts for contract deployment, to automate common
interactions, or for gas profiling."""


def main():
    args = docopt(__doc__)
    update_argv_from_docopt(args)

    if project.check_for_project():
        active_project = project.load()
        active_project.load_config()
        print(f"{active_project._name} is the active project.")
    else:
        active_project = None
        print("No project was loaded.")

    network.connect(ARGV["network"])

    run(
        args["<filename>"],
        method_name=args["<function>"] or "main",
        project=active_project,
    )
    if ARGV["gas"]:
        print_gas_profile()
