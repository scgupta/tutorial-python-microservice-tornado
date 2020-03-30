#!/usr/bin/env python

import argparse
import os
import subprocess
from typing import List
import unittest

SOURCE_CODE = ['addrservice']
TEST_CODE = ['tests']
ALL_CODE = SOURCE_CODE + TEST_CODE


def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run linter, static type checker, tests'
    )

    subparsers = parser.add_subparsers(dest='func', help='sub-commands')

    typechecker_cmd_parser = subparsers.add_parser('typecheck')
    typechecker_cmd_parser.add_argument(
        '-c', '--checker',
        default='mypy',
        help='specify static type checker, default: %(default)s'
    )
    typechecker_cmd_parser.add_argument(
        'paths',
        nargs='*',
        default=ALL_CODE,
        help='directories and files to check'
    )

    lint_cmd_parser = subparsers.add_parser('lint')
    lint_cmd_parser.add_argument(
        '-l', '--linter',
        default='flake8',
        help='specify linter, default: %(default)s'
    )
    lint_cmd_parser.add_argument(
        'paths',
        nargs='*',
        default=ALL_CODE,
        help='directories and files to check'
    )

    test_cmd_parser = subparsers.add_parser('test')
    test_cmd_parser.add_argument(
        '--suite',
        choices=['all', 'unit', 'integration'],
        default='all',
        type=str,
        help='test suite to run, default: %(default)s'
    )
    test_cmd_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='turn on verbose output'
    )

    return parser


def run_checker(checker: str, paths: List[str]) -> None:
    if len(paths) != 0:
        subprocess.call([checker] + paths)


def run_tests(suite_name: str, verbose: bool) -> None:
    test_suites = {
        'all': 'tests',
        'unit': 'tests/unit',
        'integration': 'tests/integration'
    }
    suite = test_suites.get(suite_name, 'tests')

    verbosity = 2 if verbose else 1

    test_suite = unittest.TestLoader().discover(suite, pattern='*_test.py')
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


def main(args=None) -> None:
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    parser = arg_parser()
    args = parser.parse_args(args)
    # print(args)

    actions = {
        'typecheck': lambda: run_checker(args.checker, args.paths),
        'lint': lambda: run_checker(args.linter, args.paths),
        'test': lambda: run_tests(args.suite, args.verbose),
    }

    actions.get(args.func, parser.print_help)()


if __name__ == "__main__":
    main()
