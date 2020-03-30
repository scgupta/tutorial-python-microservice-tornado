# Copyright (c) 2020. All rights reserved.

import glob
import json
import os
from typing import Dict, Sequence

ADDR_SERVICE_TEST_DATA_DIR = os.path.abspath(os.path.dirname(__file__))


ADDRESS_DATA_DIR = os.path.abspath(os.path.join(
    ADDR_SERVICE_TEST_DATA_DIR,
    'addresses'
))

ADDRESS_FILES = glob.glob(ADDRESS_DATA_DIR + '/*.json')


def address_data_suite(
    json_files: Sequence[str] = ADDRESS_FILES
) -> Dict[str, Dict]:
    addr_data_suite = {}

    for fname in json_files:
        nickname = os.path.splitext(os.path.basename(fname))[0]
        with open(fname, mode='r', encoding='utf-8') as f:
            addr_json = json.load(f)
            addr_data_suite[nickname] = addr_json

    return addr_data_suite
