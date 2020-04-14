# Copyright (c) 2020. All rights reserved.

import jsonschema  # type: ignore
import logging
from typing import AsyncIterator, Mapping, Tuple

from addrservice import ADDRESS_BOOK_SCHEMA
from addrservice.database.db_engines import create_addressbook_db
from addrservice.datamodel import AddressEntry


class AddressBookService:
    def __init__(
        self,
        config: Mapping,
        logger: logging.Logger
    ) -> None:
        self.addr_db = create_addressbook_db(config['addr-db'])
        self.logger = logger

    def start(self):
        self.addr_db.start()

    def stop(self):
        self.addr_db.stop()

    def validate_address(self, addr: Mapping) -> None:
        try:
            jsonschema.validate(addr, ADDRESS_BOOK_SCHEMA)
        except jsonschema.exceptions.ValidationError:
            raise ValueError('JSON Schema validation failed')

    async def create_address(self, value: Mapping) -> str:
        self.validate_address(value)
        addr = AddressEntry.from_api_dm(value)
        key = await self.addr_db.create_address(addr)
        return key

    async def get_address(self, key: str) -> Mapping:
        addr = await self.addr_db.read_address(key)
        return addr.to_api_dm()

    async def update_address(self, key: str, value: Mapping) -> None:
        self.validate_address(value)
        addr = AddressEntry.from_api_dm(value)
        await self.addr_db.update_address(key, addr)

    async def delete_address(self, key: str) -> None:
        await self.addr_db.delete_address(key)

    async def get_all_addresses(self) -> AsyncIterator[Tuple[str, Mapping]]:
        async for nickname, addr in self.addr_db.read_all_addresses():
            yield nickname, addr.to_api_dm()
