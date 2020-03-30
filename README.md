# Tutorial: Building, testing and profiling efficient micro-services using Tornado

## 0. Get the source code

Get the source code for the tutorial:

``` bash
$ git clone https://github.com/scgupta/tutorial-python-microservice-tornado.git
$ cd tutorial-python-microservice-tornado

$ tree .
.
├── LICENSE
├── README.md
├── addrservice
│   └── __init__.py
├── requirements.txt
├── run.py
└── tests
    ├── __init__.py
    ├── integration
    │   └── __init__.py
    └── unit
        └── __init__.py
```

The directory `addrservice` is  for the source code of the service, and the directory `test` is for keeping the tests.

## 1. Project Setup

Setup Virtual Environment:

``` bash
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip install --upgrade pip
$ pip3 install -r ./requirements.txt
```

Let's start from scratch:

``` bash
$ git checkout -b <branch> tag-01-project-setup
```

You can run static type checker, linter, unit tests, and code coverage by either executing the tool directly or through `run.py` script. In each of the following, In each of the following, you can use either of the commands.

Static Type Checker:

``` bash
$ mypy ./addrservice ./tests

$ ./run.py typecheck
```

Linter:

``` bash
$ flake8 ./addrservice ./tests

$ ./run.py lint
```

Unit Tests:

``` bash
$ python -m unittest discover tests -p '*_test.py'

$ ./run.py test
```

Code Coverage:

``` bash
$ coverage run --source=addrservice --branch -m unittest discover tests -p '*_test.py'

$ coverage run --source=addrservice --branch ./run.py test
```

After running tests with code coverage, you can get the report:

``` bash
$ coverage report
Name                      Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------
addrservice/__init__.py       2      2      0      0     0%
```

You can also generate HTML report:

``` bash
$ coverage html
$ open htmlcov/index.html
```

If you are able to run all these commands, your project setup has no error and you are all set for coding.

---
