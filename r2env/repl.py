# -*- coding: utf-8 -*-

import argparse
import sys

from r2env.tools import print_console, ERROR
from r2env.core import R2Env


HELP_MESSAGE = """
Usage: r2env [-flags] [action] [args...]

Flags:

-h, --help         - show this help
-v, --version      - display r2env version
-m, --meson        - use meson instead of acr
-p, --package      - install the dist package instead of building
-l, --list         - list available and installed packages

Actions:

init               - create .r2env in current directory
config             - display current .r2env settings
install   [pkg]    - build and install given package. Use --meson to use it as the build system.
uninstall [pkg]    - remove selected package
use [pkg]          - use r2 package defined. pkg should be a release version or latest.
path               - show path of current r2 in use
version            - show version of r2env
versions           - List all Radare versions installed
list               - list all Radare packages available to r2env
shell              - open a new shell with PATH env var set

"""


def show_help():
    print_console(HELP_MESSAGE)


def show_version():
    print_console(R2Env().version())


actions_with_argument = ["install", "uninstall", "use"]
actions_with_arguments = ["shell"]
actions = {
    "init": R2Env().init,
    "version": show_version,
    "path": R2Env().get_r2_path,
    "shell": R2Env().shell,
    "config": R2Env().show_config,
    "list": R2Env().list_packages,
    "install": R2Env().install,
    "installed": R2Env().list_installed_packages,
    "uninstall": R2Env().uninstall,
    "use": R2Env().use,
    "help": show_help
}


def run_action(argp):
    action = ""
    args = []
    if len(argp.args) > 0:
        action = argp.args[0]
    if len(argp.args) > 1:
        args = argp.args[1:]
    if argp.version:
        print_console(R2Env().version())
    elif argp.list:
        actions["list"]()
    elif action == "":
        show_help()
    elif action not in actions:
        print_console("Invalid action", ERROR)
    elif action in actions_with_arguments:
        actions[action](" ".join(args))
    elif action in actions_with_argument:
        exit_if_not_argument_is_set(args, action)
        if action == "install":
            actions[action](args[0], use_meson=argp.use_meson)
        else:
            actions[action](args[0])
    else:
        actions[action]()


def exit_if_not_argument_is_set(args, action):
    if len(args) < 1:
        if action == "use":
            print_console("[x] Package not defined. Please use 'r2env use' with one installed package. ", ERROR)
            R2Env().list_installed_packages()
        else:
            print_console("[x] Missing package argument. ( as for example: radare2@latest)", ERROR)
        print_console("[x] Missing package argument. ( as for example: radare2@latest)", ERROR)
        sys.exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", help="run specified action. (Run r2env help for more information)",
                        action="store", nargs="*", default=[])
    #parser.add_argument('args', metavar='args', nargs='+', type=str, help='Specified arguments')
    parser.add_argument("-v", "--version", dest="version", help="Show r2env version", action="store_true")
    parser.add_argument("-m", "--meson", dest="meson", help="Use meson as your build system (Use acr by default).", action="store_true")
    parser.add_argument("-p", "--package", dest="package", help="Use binary package for target system if available", action="store_true")
    parser.add_argument("-l", "--list", dest="list", help="List available and installed packages", action="store_true")
    parser.print_help = show_help
    argp = parser.parse_args()
    run_action(argp)


if __name__ == "__main__":
    main()
