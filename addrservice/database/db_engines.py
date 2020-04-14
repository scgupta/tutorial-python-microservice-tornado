# Copyright (c) 2020. All rights reserved.

from typing import Dict

from addrservice.database.addressbook_db import (
    AbstractAddressBookDB, InMemoryAddressBookDB, FilesystemAddressBookDB
)


def create_addressbook_db(addr_db_config: Dict) -> AbstractAddressBookDB:
    db_type = list(addr_db_config.keys())[0]
    db_config = addr_db_config[db_type]

    return {
        'memory': lambda cfg: InMemoryAddressBookDB(),
        'fs': lambda cfg: FilesystemAddressBookDB(cfg),
    }[db_type](db_config)
