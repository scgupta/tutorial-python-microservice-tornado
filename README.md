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
│   ├── __init__.py
│   ├── service.py
│   └── tornado
│       ├── __init__.py
│       ├── app.py
│       └── server.py
├── configs
│   └── addressbook-local.yaml
├── data
│   ├── __init__.py
│   └── addresses
│       ├── namo.json
│       └── raga.json
├── requirements.txt
├── run.py
└── tests
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   └── tornado_app_addreservice_handlers_test.py
    └── unit
        ├── __init__.py
        └── tornado_app_handlers_test.py
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

## 2. Microservice

Checkout the code:

``` bash
$ git checkout -b <branch> tag-02-microservice
```

File `addrservice/service.py` has business logic for CRUD operations for the address-book. This file is indpendent of any web service framework.
It currenly has just stubs with rudimentry implementation keeing addresses in a dictionary. It is sufficint to implement and test the REST service endpoints.

[Tornado](https://www.tornadoweb.org/) is a framework to develop Python web/microservices. It uses async effectively to achieve high number of open connections. In this tutorial, we create a `tornado.web.Application` and add `tornado.web.RequestHandlers` in file `addrservice/tornado/app.py` to serve various API endpoints for this address service. Tornado also has a rich framework for testing.

Web services return HTML back. In address book microservice, API data interface is JSON. We will examine key Tornado APIs of `Application`, `RequestHandler` and `tornado.testing` to develop it.

But first, let's run the server and test it:

``` bash
$ python3 addrservice/tornado/server.py --port 8080 --config ./configs/addressbook-local.yaml --debug

Starting Address Book on port 8080 ...
```

Also run lint, typecheck and test to verify nothing is broken, and also code coverage:

``` bash
$ ./run.py lint
$ ./run.py typecheck
$ ./run.py test -v
$ coverage run --source=addrservice --omit="addrservice/tornado/server.py" --branch ./run.py test
$ coverage report
Name                              Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------
addrservice/__init__.py               2      0      0      0   100%
addrservice/service.py               23      1      0      0    96%
addrservice/tornado/__init__.py       0      0      0      0   100%
addrservice/tornado/app.py           83      4      8      3    92%
-------------------------------------------------------------------
TOTAL                               108      5      8      3    93%
```

The `addrservice/tornado/server.py` has been omitted from coverage. This is the file used to start the server. Since Torando test framework has a mechanism to start the server in the same process where tests are running, this file does not get tested by unit and integration tests.

These are the addressbook API endpoints, implemented through two Request Handlers:

`AddressBookRequestHandler`:

- `GET /addresses`: gets all addresses in the address book
- `POST /addresses`: create an entry in the addressbook

`AddressBookEntryRequestHandler`:

- `GET /addresses/{id}`: get the address book entry with given id
- `PUT /addresses/{id}`: update the address book entry with given id
- `DELETE /addresses/{id}`: delete the address book entry with given id

Here is a sample session exercising all endpoints (notice the POST response has Location in the Headers containing the URI/id `66fdbb78e79846849608b2cfe244a858` of the entry that gets created):

``` bash
# Create an address entry

$ curl -i -X POST http://localhost:8080/addresses -d '{"full_name": "Bill Gates"}'

HTTP/1.1 201 Created
Server: TornadoServer/6.0.3
Content-Type: text/html; charset=UTF-8
Date: Tue, 10 Mar 2020 14:40:01 GMT
Location: /addresses/66fdbb78e79846849608b2cfe244a858
Content-Length: 0
Vary: Accept-Encoding

# Read the address entry

$ curl -i -X GET http://localhost:8080/addresses/66fdbb78e79846849608b2cfe244a858

HTTP/1.1 200 OK
Server: TornadoServer/6.0.3
Content-Type: application/json; charset=UTF-8
Date: Tue, 10 Mar 2020 14:44:26 GMT
Etag: "5496aee01a83cf2386641b2c43540fc5919d621e"
Content-Length: 22
Vary: Accept-Encoding
{"full_name": "Bill Gates"}

# Update the address entry

$ curl -i -X PUT http://localhost:8080/addresses/66fdbb78e79846849608b2cfe244a858 -d '{"full_name": "William Henry Gates III"}'

HTTP/1.1 204 No Content
Server: TornadoServer/6.0.3
Date: Tue, 10 Mar 2020 14:48:04 GMT
Vary: Accept-Encoding

# List all addresses

$ curl -i -X GET http://localhost:8080/addresses

HTTP/1.1 200 OK
Server: TornadoServer/6.0.3
Content-Type: application/json; charset=UTF-8
Date: Tue, 10 Mar 2020 14:49:10 GMT
Etag: "5601e676f3fa4447feaa8d2dd960be163af7570a"
Content-Length: 73
Vary: Accept-Encoding
{"66fdbb78e79846849608b2cfe244a858": {"full_name": "William Henry Gates III"}}

# Delete the address

$ curl -i -X DELETE http://localhost:8080/addresses/66fdbb78e79846849608b2cfe244a858

HTTP/1.1 204 No Content
Server: TornadoServer/6.0.3
Date: Tue, 10 Mar 2020 14:50:38 GMT
Vary: Accept-Encoding

# Verify address is deleted

$ curl -i -X GET http://localhost:8080/addresses

HTTP/1.1 200 OK
Server: TornadoServer/6.0.3
Content-Type: application/json; charset=UTF-8
Date: Tue, 10 Mar 2020 14:52:01 GMT
Etag: "bf21a9e8fbc5a3846fb05b4fa0859e0917b2202f"
Content-Length: 2
Vary: Accept-Encoding
{}

$ curl -i -X GET http://localhost:8080/addresses/66fdbb78e79846849608b2cfe244a858 

HTTP/1.1 404 '66fdbb78e79846849608b2cfe244a858'
Server: TornadoServer/6.0.3
Content-Type: application/json; charset=UTF-8
Date: Tue, 10 Mar 2020 14:53:06 GMT
Content-Length: 1071
Vary: Accept-Encoding
{"method": "GET", "uri": "/addresses/66fdbb78e79846849608b2cfe244a858", "code": 404, "message": "'66fdbb78e79846849608b2cfe244a858'", "trace": "Traceback (most recent call last):\n\n  File \"... redacted call stack trace ... addrservice/tornado/app.py\", line 100, in get\n    raise tornado.web.HTTPError(404, reason=str(e))\n\ntornado.web.HTTPError: HTTP 404: '66fdbb78e79846849608b2cfe244a858'\n"}
```

---
