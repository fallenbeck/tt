#!/usr/bin/env python3
# This is a script intended to track your project activities.
# It is really simple and I got the idea when using todolist on the command
# line. tymetracker (tt) is written entirely in Python 3 and stores the
# records in a json data structure in the user's home directory.
#
datafile = "~/.tymetracker.json"

### Here be dragons
# Sanity check: only proceed if we are in a python3 environment
import sys
if not str(sys.version).startswith("3"):
    print("Python 3 is required to run tymetracker/tt.")
    sys.exit(1)

# Import stuff we need
import json
import os

# Set variables we need
n = "tymetracker/tt"
f = os.path.abspath(os.path.expanduser(datafile))

class bcolors:
    """Define some colors that can be used in the terminal.
    """
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def init():
    '''Initialize a new datafile.
    '''
    if os.path.isfile(f):
        print("Data file {} already exists".format(f))
        sys.exit(2)
    else:
        print("Initializing new data file {}".format(f))

        # Initialize new data dict
        data = {
                "projects": {},
                }

        # ... and write it to data file
        save(data)

def load():
    try:
        fp = open(f, "r")
        data = json.load(fp)
        fp.close()
    except FileNotFoundError as e:
        print("Could not load data file. Please run", bcolors.YELLOW, "init", bcolors.END, "first.")
        sys.exit(3)
    except Exception as e:
        print(e)
        sys.exit(4)

    if data is None:
        print("Read corrupt data from", f)
        sys.exit(6)

    return data

def save(data):
    if data is not None:
        try:
            fp = open(f, "w")
            json.dump(data, fp)
            fp.flush()
            fp.close()
        except Exception as e:
            print(e)
            sys.exit(5)
    else:
        print("No data to write")

def usage():
    """Print the list of commands that are supported. This function is
    called if the users calls tt with no or too few arguments.
    """
    group = {
            "Generic commands": {
                "init": "Initialize new data file",
                },
            "Projects": {
                #"DESC": "Projects are needed for time tracking",
                "ap project name": "Add new project with name \"project name\"",
                "dp 23": "Delete project with id 23",
                "lp": "List projects and their ids",
                },
            "Tracking": {
                #"DESC": "Time tracking is about time tracking",
                "start 23": "Starts time tracking for project id 23",
                "stop": "Stops active time tracking",
                "show 23": "Show tracked times for project 23",
                "rep 23": "Show a report for project 23",
                }
            }

    # Display the commands/dicts
    for group, commands in sorted(group.items()):
        print(bcolors.PURPLE, "\n{group}".format(group=group), bcolors.END)

        # print the DESC if needed
        if "DESC" in commands:
            print("{desc}".format(desc=commands["DESC"]))

        # print all commands (and not DESC)
        for command, description in sorted(commands.items()):
            if command is not "DESC":
                print(bcolors.YELLOW, "    {cmd:20s}".format(cmd=command), bcolors.END, description)

def list_projects():
    data = load()
    p = data.get("projects", {})

    if len(p) == 0:
        print("No projects found.")
        #print("Create a new project with", bcolors.YELLOW, "ap project name", bcolors.END, "first.")
    else:
        print("Found {num} projects:\n{p}".format(num=len(p), p=p))

def add_project():
    if len(sys.argv) < 3:
        print("You must specify a project name")
        sys.exit(10)

    name = " ".join(sys.argv[2:]).strip()
    data = load()
    projects = data.get("projects", {})
    # TODO: create unique ID for project
    projects[1] = name
    data["projects"] = projects
    print(data)
    save(data)


def main():
    """Main function that handles the run of tymetracker.
    Parses the arguments and calls the appropriate functions.
    """
    if len(sys.argv) <= 1:
        usage()
    elif sys.argv[1].lower() == "init":
        init()
    elif sys.argv[1].lower() == "lp":
        list_projects()
    elif sys.argv[1].lower() == "ap":
        add_project()
    else:
        usage()


# Starting here
main()