# Copyright (c) 2020. All rights reserved.

import json
import logging
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Dict,
    Optional,
    Tuple,
    Type,
)
import traceback
import uuid

import tornado.web

from addrservice import LOGGER_NAME
from addrservice.service import AddressBookService
import addrservice.utils.logutils as logutils

ADDRESSBOOK_REGEX = r'/addresses/?'
ADDRESSBOOK_ENTRY_REGEX = r'/addresses/(?P<id>[a-zA-Z0-9-]+)/?'
ADDRESSBOOK_ENTRY_URI_FORMAT_STR = r'/addresses/{id}'


class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(
        self,
        service: AddressBookService,
        config: Dict,
        logger: logging.Logger
    ) -> None:
        self.service = service
        self.config = config
        self.logger = logger

    def prepare(self) -> Optional[Awaitable[None]]:
        req_id = uuid.uuid4().hex
        logutils.set_log_context(
            req_id=req_id,
            method=self.request.method,
            uri=self.request.uri,
            ip=self.request.remote_ip
        )

        logutils.log(
            self.logger,
            logging.DEBUG,
            include_context=True,
            message='REQUEST'
        )

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

        logutils.set_log_context(reason=self._reason)

        if 'exc_info' in kwargs:
            exc_info = kwargs['exc_info']
            logutils.set_log_context(exc_info=exc_info)
            if self.settings.get('serve_traceback'):
                # in debug mode, send a traceback
                trace = '\n'.join(traceback.format_exception(*exc_info))
                body['trace'] = trace

        self.finish(body)

    def log_exception(
        self,
        typ: Optional[Type[BaseException]],
        value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        # https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.log_exception
        if isinstance(value, tornado.web.HTTPError):
            if value.log_message:
                msg = value.log_message % value.args
                logutils.log(
                    tornado.log.gen_log,
                    logging.WARNING,
                    status=value.status_code,
                    request_summary=self._request_summary(),
                    message=msg
                )
        else:
            logutils.log(
                tornado.log.app_log,
                logging.ERROR,
                message='Uncaught exception',
                request_summary=self._request_summary(),
                request=repr(self.request),
                exc_info=(typ, value, tb)
            )


class DefaultRequestHandler(BaseRequestHandler):
    def initialize(  # type: ignore
        self,
        status_code: int,
        message: str,
        logger: logging.Logger
    ):
        self.logger = logger
        self.set_status(status_code, reason=message)

    def prepare(self) -> Optional[Awaitable[None]]:
        raise tornado.web.HTTPError(
            self._status_code,
            'request uri: %s',
            self.request.uri,
            reason=self._reason
        )


class AddressBookRequestHandler(BaseRequestHandler):
    async def get(self):
        all_addrs = {}
        async for nickname, addr in self.service.get_all_addresses():
            all_addrs[nickname] = addr

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
    # https://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings

    logger = getattr(handler, 'logger', logging.getLogger(LOGGER_NAME))

    if handler.get_status() < 400:
        level = logging.INFO
    elif handler.get_status() < 500:
        level = logging.WARNING
    else:
        level = logging.ERROR

    logutils.log(
        logger,
        level,
        include_context=True,
        message='RESPONSE',
        status=handler.get_status(),
        time_ms=(1000.0 * handler.request.request_time())
    )

    logutils.clear_log_context()


def make_addrservice_app(
    config: Dict,
    debug: bool,
    logger: logging.Logger
) -> Tuple[AddressBookService, tornado.web.Application]:
    service = AddressBookService(config, logger)

    app = tornado.web.Application(
        [
            # Address Book endpoints
            (ADDRESSBOOK_REGEX, AddressBookRequestHandler,
                dict(service=service, config=config, logger=logger)),
            (ADDRESSBOOK_ENTRY_REGEX, AddressBookEntryRequestHandler,
                dict(service=service, config=config, logger=logger))
        ],
        compress_response=True,  # compress textual responses
        log_function=log_function,  # log_request() uses it to log results
        serve_traceback=debug,  # it is passed on as setting to write_error()
        default_handler_class=DefaultRequestHandler,
        default_handler_args={
            'status_code': 404,
            'message': 'Unknown Endpoint',
            'logger': logger
        }
    )

    return service, app
