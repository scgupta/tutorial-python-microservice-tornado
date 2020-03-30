# Copyright (c) 2020. All rights reserved.

import json
from typing import (
    Any,
    Awaitable,
    Dict,
    Optional,
    Tuple,
)
import traceback

import tornado.web

from addrservice.service import AddressBookService

ADDRESSBOOK_REGEX = r'/addresses/?'
ADDRESSBOOK_ENTRY_REGEX = r'/addresses/(?P<id>[a-zA-Z0-9-]+)/?'
ADDRESSBOOK_ENTRY_URI_FORMAT_STR = r'/addresses/{id}'


class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(
        self,
        service: AddressBookService,
        config: Dict
    ) -> None:
        self.service = service
        self.config = config

    def prepare(self) -> Optional[Awaitable[None]]:
        msg = 'REQUEST: {method} {uri} ({ip})'.format(
            method=self.request.method,
            uri=self.request.uri,
            ip=self.request.remote_ip
        )
        print(msg)

        return super().prepare()

    def on_finish(self) -> None:
        super().on_finish()

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        body = {
            'method': self.request.method,
            'uri': self.request.path,
            'code': status_code,
            'message': self._reason
        }

        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, send a traceback
            trace = '\n'.join(traceback.format_exception(*kwargs['exc_info']))
            body['trace'] = trace

        self.finish(body)


class DefaultRequestHandler(BaseRequestHandler):
    def initialize(self, status_code, message):
        self.set_status(status_code, reason=message)

    def prepare(self) -> Optional[Awaitable[None]]:
        raise tornado.web.HTTPError(
            self._status_code, reason=self._reason
        )


class AddressBookRequestHandler(BaseRequestHandler):
    async def get(self):
        all_addrs = await self.service.get_all_addresses()
        self.set_status(200)
        self.finish(all_addrs)

    async def post(self):
        try:
            addr = json.loads(self.request.body.decode('utf-8'))
            id = await self.service.create_address(addr)
            addr_uri = ADDRESSBOOK_ENTRY_URI_FORMAT_STR.format(id=id)
            self.set_status(201)
            self.set_header('Location', addr_uri)
            self.finish()
        except (json.decoder.JSONDecodeError, TypeError):
            raise tornado.web.HTTPError(
                400, reason='Invalid JSON body'
            )
        except ValueError as e:
            raise tornado.web.HTTPError(400, reason=str(e))


class AddressBookEntryRequestHandler(BaseRequestHandler):
    async def get(self, id):
        try:
            addr = await self.service.get_address(id)
            self.set_status(200)
            self.finish(addr)
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))

    async def put(self, id):
        try:
            addr = json.loads(self.request.body.decode('utf-8'))
            await self.service.update_address(id, addr)
            self.set_status(204)
            self.finish()
        except (json.decoder.JSONDecodeError, TypeError):
            raise tornado.web.HTTPError(
                400, reason='Invalid JSON body'
            )
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))
        except ValueError as e:
            raise tornado.web.HTTPError(400, reason=str(e))

    async def delete(self, id):
        try:
            await self.service.delete_address(id)
            self.set_status(204)
            self.finish()
        except KeyError as e:
            raise tornado.web.HTTPError(404, reason=str(e))


def log_function(handler: tornado.web.RequestHandler) -> None:
    status = handler.get_status()
    request_time = 1000.0 * handler.request.request_time()

    msg = 'RESPOSE: {status} {method} {uri} ({ip}) {time}ms'.format(
        status=status,
        method=handler.request.method,
        uri=handler.request.uri,
        ip=handler.request.remote_ip,
        time=request_time,
    )

    print(msg)


def make_addrservice_app(
    config: Dict,
    debug: bool
) -> Tuple[AddressBookService, tornado.web.Application]:
    service = AddressBookService(config)

    app = tornado.web.Application(
        [
            # Address Book endpoints
            (ADDRESSBOOK_REGEX, AddressBookRequestHandler,
                dict(service=service, config=config)),
            (ADDRESSBOOK_ENTRY_REGEX, AddressBookEntryRequestHandler,
                dict(service=service, config=config))
        ],
        compress_response=True,  # compress textual responses
        log_function=log_function,  # log_request() uses it to log results
        serve_traceback=debug,  # it is passed on as setting to write_error()
        default_handler_class=DefaultRequestHandler,
        default_handler_args={
            'status_code': 404,
            'message': 'Unknown Endpoint'
        }
    )

    return service, app
