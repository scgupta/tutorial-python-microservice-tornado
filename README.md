# Tutorial: Building and testing micro-services using Tornado

Blog Posts:

1. [Choices, Key Concepts, and Project setup](https://www.ml4devs.com/articles/python-microservices-tornado-01-asyncio-lint-test-coverage-project-setup/)
2. [Build and Test REST Endpoints With Tornado](https://www.ml4devs.com/articles/python-microservices-tornado-02-rest-unit-integration-tests/)
3. [Effective Canonical Logging Across Services](https://www.ml4devs.com/articles/python-microservices-tornado-03-effective-canonical-logging-across-services/)
4. [API, Object, and Storage Data Models](https://www.ml4devs.com/articles/python-microservices-tornado-04-api-object-and-physical-storage-data-models/)

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
│   ├── database
│   │   ├── __init__.py
│   │   ├── addressbook_db.py
│   │   └── db_engines.py
│   ├── datamodel.py
│   ├── service.py
│   ├── tornado
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── server.py
│   └── utils
│       ├── __init__.py
│       └── logutils.py
├── configs
│   └── addressbook-local.yaml
├── data
│   ├── __init__.py
│   └── addresses
│       ├── namo.json
│       └── raga.json
├── requirements.txt
├── run.py
├── schema
│   └── address-book-v1.0.json
└── tests
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   ├── addrservice_test.py
    │   └── tornado_app_addreservice_handlers_test.py
    └── unit
        ├── __init__.py
        ├── address_data_test.py
        ├── addressbook_db_test.py
        ├── datamodel_test.py
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

## 3. Logging

Checkout the code:

``` bash
$ git checkout -b <branch> tag-03-logging
```

Effective logs can cut down diagnosis time and facilitate monitoring and altering.

### Log Format

[Logfmt](https://pypi.org/project/logfmt/) log format consists of *key-value* pairs.
It offers good balance between processing using standard tools and human readibility.

### Canonical Logs

Emiting one canonical log line](https://brandur.org/canonical-log-lines) for each request makes manual inspection easier.
Assigning and logging a *request id* to each request, and passing that id to all called service helps correlate logs across services.
The *key-value* pairs for the log are stored in a [task context](https://github.com/Skyscanner/aiotask-context), which is maintained across asyncio task interleaving.

### Log Configuration

Logging are useful in diagnosing services, more so when async is involved. Python has a standard [logging](https://docs.python.org/3/library/logging.html) package, and its documentation includes an excellent [HOWTO](https://docs.python.org/3/howto/logging.html) guide and [Cookbook](https://docs.python.org/3/howto/logging-cookbook.html). These are rich source of information, and leave nothoing much to add. Following are some of the best practices in my opinion:

- Do NOT use ROOT logger directly throgh `logging.debug()`, `logging.error()` methods directly because it is easy to overlook their default behavior.
- Do NOT use module level loggers of variety `logging.getLogger(__name__)` because any complex project will require controlling logging through configuration (see next point). These may cause surprise if you forget to set `disable_existing_loggers` to false or overlook how modules are loaded and initialized. If use at all, call `logging.getLogger(__name__)` inside function, rather than outside at the beginning of a module.
- `dictConfig` (in `yaml`) offers right balance of versatility and flexibility compared to `ini` based `fileConfig`or doing it in code. Specifying logger in config files allows you to use different logging levels and infra in prod deployment, stage deployments, and local debugging (with increasingly more logs).

Sending logs to multiple data stores and tools for processing can be controled by a [log configuration](https://docs.python.org/3/library/logging.config.html). Each logger has a format and multiple handlers can be associated with a logger. Here is a part of `configs/addressbook-local.yaml`:

``` yaml
logging:
  version: 1
  formatters:
    brief:
      format: '%(asctime)s %(name)s %(levelname)s : %(message)s'
    detailed:
      format: 'time="%(asctime)s" logger="%(name)s" level="%(levelname)s" file="%(filename)s" lineno=%(lineno)d function="%(funcName)s" %(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      formatter: brief
      stream: ext://sys.stdout
    file:
      class : logging.handlers.RotatingFileHandler
      level: DEBUG
      formatter: detailed
      filename: /tmp/addrservice-app.log
      backupCount: 3
  loggers:
    addrservice:
      level: DEBUG
      handlers:
        - console
        - file
      propagate: no
    tornado.access:
      level: DEBUG
      handlers:
        - file
    tornado.application:
      level: DEBUG
      handlers:
        - file
    tornado.general:
      level: DEBUG
      handlers:
        - file
  root:
    level: WARNING
    handlers:
      - console
```

Notice that this configuration not just defines a logger `addrservice` for this service, but also modifies behavior of Tornado's general logger. There are several pre-defined [handlers](https://docs.python.org/3/library/logging.handlers.html). Here the SteamHandler and RotatingFileHandler are being used to write to console and log files respectively.

### Tornado

Tornado has several hooks to control when and how logging is done:

- [`log_function`](https://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings): function Tornado calls at the end of every request to log the result.
- [`write_error`](https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write_error): to customize the error response. Information about the error is added to the log context.
- [`log_exception`](): to log uncaught exceptions. It can be overwritten to log in logfmt format.

### Log Inspection

**Start the server:**

It will show the console log:

``` bash
$ python3 addrservice/tornado/server.py --port 8080 --config ./configs/addressbook-local.yaml --debug

2020-03-17 12:54:15,198 addrservice INFO : message="STARTING" service_name="Address Book" port=8080
```

**Watch the logs:**

``` bash
$ tail -f /tmp/addrservice-app.log

time="2020-03-17 12:54:15,198" logger="addrservice" level="INFO" file="logutils.py" lineno=57 function="log" message="STARTING" service_name="Address Book" port=8080
```

**Send a request:**

```bash
$ curl -i -X POST http://localhost:8080/addresses -d '{"name": "Bill Gates"}'

HTTP/1.1 201 Created
Server: TornadoServer/6.0.3
Content-Type: text/html; charset=UTF-8
Date: Tue, 17 Mar 2020 07:26:32 GMT
Location: /addresses/7feec2df29fd4b039028ad351bafe422
Content-Length: 0
Vary: Accept-Encoding
```

The console log will show brief log entries:

``` log
2020-03-17 12:56:32,784 addrservice INFO : req_id="e6cd3072530f46b9932946fd65a13779" method="POST" uri="/addresses" ip="::1" message="RESPONSE" status=201 time_ms=1.2888908386230469
```

The log file will show logfmt-style one-line detailed canonical log entries:

``` log
time="2020-03-17 12:56:32,784" logger="addrservice" level="INFO" file="logutils.py" lineno=57 function="log" req_id="e6cd3072530f46b9932946fd65a13779" method="POST" uri="/addresses" ip="::1" message="RESPONSE" status=201 time_ms=1.2888908386230469
```

### Unit and Integration Tests

Tests are quiet by default:

``` bash
$ ./run.py lint
$ ./run.py typecheck

$ ./run.py test -v

test_address_book_endpoints (integration.tornado_app_addreservice_handlers_test.TestAddressServiceApp) ... ok
test_default_handler (unit.tornado_app_handlers_test.AddressServiceTornadoAppUnitTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.049s

OK

$ coverage run --source=addrservice --omit="addrservice/tornado/server.py" --branch ./run.py test

..
----------------------------------------------------------------------
Ran 2 tests in 0.049s
OK

$ coverage report

Name                              Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------
addrservice/__init__.py               3      0      0      0   100%
addrservice/service.py               25      1      0      0    96%
addrservice/tornado/__init__.py       0      0      0      0   100%
addrservice/tornado/app.py          105      6     18      6    90%
addrservice/utils/__init__.py         0      0      0      0   100%
addrservice/utils/logutils.py        28      0      6      0   100%
-------------------------------------------------------------------
TOTAL                               161      7     24      6    93%
```

If you want to change the log message during tests, change log level from ERROR to INFO:

``` python
# tests/unit/tornado_app_handlers_test.py

IN_MEMORY_CFG_TXT = '''
service:
  name: Address Book Test
logging:
  version: 1
  root:
    level: INFO
'''
```

With that change, if you run the tests, you can examine the logs:

``` log
$ ./run.py tests

INFO:addrservice:req_id="a100e35140604d72930cb16c9eed8e8a" method="GET" uri="/addresses/" ip="127.0.0.1" message="RESPONSE" status=200 time_ms=1.232147216796875
INFO:addrservice:req_id="29b08c81acbd403b89f007ba03b5fee7" method="POST" uri="/addresses/" ip="127.0.0.1" message="RESPONSE" status=201 time_ms=0.9398460388183594
WARNING:addrservice:req_id="1c959a77f9de4f7e87e384a174fb6fbe" method="POST" uri="/addresses/" ip="127.0.0.1" reason="Invalid JSON body" message="RESPONSE" status=400 time_ms=1.7652511596679688 trace="Traceback.....
```

---

## 4. Data Model

Get the code:

``` bash
$ git checkout -b <branch> tag-04-datamodel
```

### API Data Model

Also known as communication or exchange data model
The data model for interacting with a microservice. It is designed for efficiently exchanging (sending and receiving) data with the service.

The address book service uses JSON for exchanging data. The [JSON schema](https://json-schema.org/) for the data model is in `schema/address-book-v1.0.json`, and test data in `data/addresses/*.json`. Even the data must be tested to be correct. So there is a test `tests/unit/address_data_test.py` to check whether data files conform to the JSON schema.

``` bash
$ python3 tests/unit/address_data_test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.006s

OK
```

### Object Data Model

Also known as application data model or data structures.
It is designed for efficiently performing business logic (algorithms) of an application / service.

There are tools like [Python JSON Schema Objects](https://github.com/cwacek/python-jsonschema-objects), [Warlock](https://github.com/bcwaldon/warlock), [Valideer](https://github.com/podio/valideer), that generate POPO (Plain Old Python Object) classes from a JSON schema. These tools do simple structural mapping from JSON schema elements to classes. However, there are validation checks, inheritance, and polymorphism that can't be expressed in JSON schema. So it may require hand-crafting a data model suitable for business logic.

The logical data model is implemented in `addrservice/datamodel.py`.

### Storage Data Model

Also known as Physical Data Model.
It is designed for efficient storage, retrieval, and search. There are several kinds of data stores: relational, hierarchical, graph. A combination of these storage is picked depending upon the structure of the persistent data, and retrieval and search requirements.

The `addrservice/database/addressbook_db.py` defines an `AbstractAddressBookDB`, which the service interacts with. This decouples the storage choice, and allows changing the storage model without affecting rest of the code. For example, it defines an `InMemoryAddressBookDB` and `FileAddressBookDB`. The in-memory data store is useful in unit/integration tests as it facilitates deep asserts for the state of the store. The file backed storage persists the data in files, and useful for debugging.

The storage can be swapped by setting the configuration, for example:

``` yaml
addr-db:
  memory: null
```

Based on the config, an appropriate DB engine is set up by `addrservice/database/db_engines.py:create_addressbook_db()`.

Following is need to implement a SQL data store:

- Implement a sub-class of `AbstractAddressBookDB` that stores data in a RDBMS
- Add a case in `create_addressbook_db()`
- Change config (`configs/addressbook-local.yaml`)

It does not require touch any of the business logic.

### Running the Service

Start the service:

``` bash
$ python3 addrservice/tornado/server.py --port 8080 --config ./configs/addressbook-local.yaml --debug

2020-03-30 06:46:29,641 addrservice INFO : message="STARTING" service_name="Address Book" port=8080
```

Test CRUD with curl command:

``` bash
$ curl -X 'GET' http://localhost:8080/addresses

{}

$ curl -i -X 'POST' -H "Content-Type: application/json" -d "@data/addresses/namo.json" http://localhost:8080/addresses

HTTP/1.1 100 (Continue)

HTTP/1.1 201 Created
Server: TornadoServer/6.0.3
Content-Type: text/html; charset=UTF-8
Date: Mon, 30 Mar 2020 01:22:10 GMT
Location: /addresses/0bc13fbf2db54ef392a08a37378afa7f
Content-Length: 0
Vary: Accept-Encoding

$ curl -X 'GET' http://localhost:8080/addresses/0bc13fbf2db54ef392a08a37378afa7f

{"full_name": "Narendra Modi", "addresses": ...}

$ curl -i -X 'PUT' -H "Content-Type: application/json" -d "@data/addresses/raga.json" http://localhost:8080/addresses/0bc13fbf2db54ef392a08a37378afa7f

HTTP/1.1 204 No Content
Server: TornadoServer/6.0.3
Date: Mon, 30 Mar 2020 01:24:51 GMT
Vary: Accept-Encoding

$ curl -X 'GET' http://localhost:8080/addresses/0bc13fbf2db54ef392a08a37378afa7f

{"full_name": "Rahul Gandhi", "addresses": ...}

$ curl -i -X 'DELETE' http://localhost:8080/addresses/0bc13fbf2db54ef392a08a37378afa7f

HTTP/1.1 204 No Content
Server: TornadoServer/6.0.3
Date: Mon, 30 Mar 2020 01:26:34 GMT
Vary: Accept-Encoding

$ curl -X 'GET' http://localhost:8080/addresses

{}
```

Change `addr-db` in `configs/addressbook-local.yaml` from memory to file system:

``` yaml
addr-db:
  fs: /tmp/addrservice-db
```

Run all the commands again. You will see records being stored in `/tmp/addrservice-db` as json files.

### Tests and Code Coverage

Run tests and check code coverage:

``` bash
$ coverage run --source=addrservice --omit="addrservice/tornado/server.py" --branch ./run.py test

..........
----------------------------------------------------------------------
Ran 10 tests in 0.148s

OK

$ coverage report

Name                                     Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
addrservice/__init__.py                      7      0      0      0   100%
addrservice/database/__init__.py             0      0      0      0   100%
addrservice/database/addressbook_db.py     107      5     28      1    96%
addrservice/database/db_engines.py           6      0      2      0   100%
addrservice/datamodel.py                   226      0     54      0   100%
addrservice/service.py                      36      0      2      0   100%
addrservice/tornado/__init__.py              0      0      0      0   100%
addrservice/tornado/app.py                 107      2     20      4    95%
addrservice/utils/__init__.py                0      0      0      0   100%
addrservice/utils/logutils.py               28      0      6      0   100%
--------------------------------------------------------------------------
TOTAL                                      517      7    112      5    98%
```

---
