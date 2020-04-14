# Copyright (c) 2020. All rights reserved.

import json
import os

ADDR_SERVICE_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ADDRESS_BOOK_SCHEMA_FILE = os.path.abspath(os.path.join(
    ADDR_SERVICE_ROOT_DIR,
    '../schema/address-book-v1.0.json'
))

with open(ADDRESS_BOOK_SCHEMA_FILE, mode='r', encoding='utf-8') as f:
    ADDRESS_BOOK_SCHEMA = json.load(f)

LOGGER_NAME = 'addrservice'
