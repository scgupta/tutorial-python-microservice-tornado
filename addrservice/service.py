# Copyright (c) 2020. All rights reserved.

import logging
from typing import Dict
import uuid


class AddressBookService:
    def __init__(
        self,
        config: Dict,
        logger: logging.Logger
    ) -> None:
        # TODO FIXME full class is just dummy stubs
        self.addrs: Dict[str, Dict] = {}
        self.logger = logger

    def start(self):
        # TODO FIXME
        self.addrs = {}

    def stop(self):
        # TODO FIXME
        pass

    async def create_address(self, value: Dict) -> str:
        # TODO FIXME
        key = uuid.uuid4().hex
        self.addrs[key] = value
        return key

    async def get_address(self, key: str) -> Dict:
        # TODO FIXME
        return self.addrs[key]

    async def update_address(self, key: str, value: Dict) -> None:
        # TODO FIXME
        self.addrs[key]  # will cause exception if key doesn't exist
        self.addrs[key] = value

    async def delete_address(self, key: str) -> None:
        self.addrs[key]  # will cause exception if key doesn't exist
        del self.addrs[key]

    async def get_all_addresses(self) -> Dict[str, Dict]:
        # TODO FIXME
        return self.addrs
