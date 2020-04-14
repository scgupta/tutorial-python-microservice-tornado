# Copyright (c) 2020. All rights reserved.

import jsonschema  # type: ignore
import unittest

from addrservice import ADDRESS_BOOK_SCHEMA
from data import address_data_suite
import addrservice.datamodel as datamodel


class AddressDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.address_data = address_data_suite()

    def test_json_schema(self) -> None:
        # Validate Address Schema
        jsonschema.Draft7Validator.check_schema(ADDRESS_BOOK_SCHEMA)

    def test_address_data_json(self) -> None:
        # Validate Address Test Data
        for nickname, addr in self.address_data.items():
            # validate using application subschema
            jsonschema.validate(addr, ADDRESS_BOOK_SCHEMA)

            # Roundrtrip Test
            addr_obj = datamodel.AddressEntry.from_api_dm(addr)
            addr_dict = addr_obj.to_api_dm()
            self.assertEqual(addr, addr_dict)


if __name__ == '__main__':
    unittest.main()
