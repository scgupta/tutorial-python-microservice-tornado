# Copyright (c) 2020. All rights reserved.

import argparse
import asyncio
from typing import Dict
import yaml

import tornado.web

from addrservice.service import AddressBookService
from addrservice.tornado.app import make_addrservice_app


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Run Address Book Server'
    )

    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=8080,
        help='port number for %(prog)s server to listen; '
        'default: %(default)s'
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='turn on debug logging'
    )

    parser.add_argument(
        '-c',
        '--config',
        required=True,
        type=argparse.FileType('r'),
        help='config file for %(prog)s'
    )

    args = parser.parse_args(args)
    return args


def run_server(
    app: tornado.web.Application,
    service: AddressBookService,
    config: Dict,
    port: int,
    debug: bool,
):
    name = config['service']['name']
    loop = asyncio.get_event_loop()

    # Start AddressBook service
    service.start()

    # Bind http server to port
    http_server_args = {
        'decompress_request': True
    }
    http_server = app.listen(port, '', **http_server_args)
    msg = 'Starting {} on port {} ...'.format(name, port)
    print(msg)

    try:
        # Start asyncio IO event loop
        loop.run_forever()
    except KeyboardInterrupt:
        # signal.SIGINT
        pass
    finally:
        loop.stop()
        msg = 'Shutting down {}...'.format(name)
        print(msg)
        http_server.stop()
        # loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
        loop.run_until_complete(loop.shutdown_asyncgens())
        service.stop()
        loop.close()
        msg = 'Stopped {}.'.format(name)
        print(msg)


def main(args=parse_args()):
    '''
    Starts the Tornado server serving Address Book on the given port
    '''

    config = yaml.load(args.config.read(), Loader=yaml.SafeLoader)

    addr_service, addr_app = make_addrservice_app(config, args.debug)

    run_server(
        app=addr_app,
        service=addr_service,
        config=config,
        port=args.port,
        debug=args.debug,
    )


if __name__ == '__main__':
    main()
