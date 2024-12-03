import json
import argparse
import os
import importlib
import sys
import subprocess


EXAMPLE_GENERATOR_FILE = 'example_generator.py'
EXAMPLES_FILE = 'labeled-examples.json'


class CheckArgAction(argparse.Action):
    def __call__(self, parser, namespace, arg, option_string=None):
        if not arg.endswith('.py'):
            raise ValueError(f"File is not a .py file.")
        if not os.path.exists(arg):
            raise ValueError(f"File {arg} doesn't exist.")
        try:
            setattr(namespace, self.dest, importlib.import_module(arg.split('.')[0]))
        except Exception as e:
            raise ValueError(str(e))

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--module', help='Python module that contains function "report_safe".', action=CheckArgAction, required=True)
args = arg_parser.parse_args()

if __name__ == '__main__':
    if not os.path.exists(EXAMPLES_FILE):
        print("Generating examples...")
        command = [sys.executable, EXAMPLE_GENERATOR_FILE]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        print(f"Examples written to file: {EXAMPLES_FILE}")
    else:
        print("Examples file found.")

    print("Loading examples...")
    with open(EXAMPLES_FILE, 'r') as f:
        labeled_examples = json.load(f)

    failed = 0
    for labeled_example in labeled_examples:
        report = labeled_example['report']
        safe = labeled_example['safe']

        if args.module.report_safe(report) != safe:
            if not failed:
                print("FAILED:\n")
            failed += 1
            print(f"{report} should be {'safe' if safe else 'not safe'}")

    if not failed:
        print("PASSED")
    else:
        print(f"Tests failed {failed} / {len(labeled_examples)}.")
