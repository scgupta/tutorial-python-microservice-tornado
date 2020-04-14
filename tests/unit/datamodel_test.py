# Copyright (c) 2020. All rights reserved.

import unittest

from addrservice.datamodel import (
    AddressType, Address, Phone, Email, AddressEntry
)


class DataModelTest(unittest.TestCase):
    def test_data_model(self) -> None:
        address = Address(
            kind=AddressType.work,
            building_name='Data Model',
            unit_number=101,
            street_number=4,
            street_name='Microservices Ave',
            locality='Python',
            city='Bangalore',
            province='Karnataka',
            pincode=560001,
            country='India'
        )
        self.assertEqual(address.kind, AddressType.work)
        self.assertEqual(address.building_name, 'Data Model')
        self.assertEqual(address.unit_number, 101)
        self.assertEqual(address.street_number, 4)
        self.assertEqual(address.street_name, 'Microservices Ave')
        self.assertEqual(address.locality, 'Python')
        self.assertEqual(address.city, 'Bangalore')
        self.assertEqual(address.province, 'Karnataka')
        self.assertEqual(address.pincode, 560001)
        self.assertEqual(address.country, 'India')

        phone = Phone(
            kind=AddressType.home,
            country_code=91,
            local_number=9876543210
        )
        self.assertEqual(phone.kind, AddressType.home)
        self.assertEqual(phone.country_code, 91)
        self.assertEqual(phone.area_code, None)
        self.assertEqual(phone.local_number, 9876543210)

        fax = Phone(
            kind=AddressType.work,
            country_code=91,
            area_code=80,
            local_number=12345678
        )
        self.assertEqual(fax.kind, AddressType.work)
        self.assertEqual(fax.country_code, 91)
        self.assertEqual(fax.area_code, 80)
        self.assertEqual(fax.local_number, 12345678)

        email = Email(
            kind=AddressType.work,
            email='datamodel@microservices.py'
        )

        address_entry = AddressEntry(
            full_name='Data Model',
            addresses=[address],
            phone_numbers=[phone],
            fax_numbers=[fax],
            emails=[email]
        )
        self.assertEqual(address_entry.full_name, 'Data Model')
        self.assertEqual(len(address_entry.addresses), 1)
        self.assertEqual(address_entry.addresses[0], address)
        self.assertEqual(len(address_entry.phone_numbers), 1)
        self.assertEqual(address_entry.phone_numbers[0], phone)
        self.assertEqual(len(address_entry.fax_numbers), 1)
        self.assertEqual(address_entry.fax_numbers[0], fax)
        self.assertEqual(len(address_entry.emails), 1)
        self.assertEqual(address_entry.emails[0], email)

        address_dict_1 = address_entry.to_api_dm()
        address_dict_2 = AddressEntry.from_api_dm(address_dict_1).to_api_dm()
        self.assertEqual(address_dict_1, address_dict_2)

        # Setters

        address.kind = AddressType.home
        address.building_name = 'Abc'
        address.unit_number = 1
        address.street_number = 2
        address.street_name = 'Xyz'
        address.locality = 'Pqr'
        address.city = 'Nowhere'
        address.province = 'Wierd'
        address.pincode = '0X01'
        address.country = 'Forsaken'

        phone.kind = AddressType.work
        phone.country_code = 1
        phone.area_code = 123
        phone.local_number = 4567890

        email.kind = AddressType.home
        email.email = 'abc@example.com'

        address_entry.full_name = 'Abc Xyz'
        address_entry.addresses = []
        address_entry.phone_numbers = []
        address_entry.fax_numbers = []
        address_entry.emails = []

        # Exceptions

        with self.assertRaises(ValueError):
            Address(
                kind=None,  # type: ignore
                street_name='Microservices Ave',
                pincode=560001,
                country='India'
            )

        with self.assertRaises(ValueError):
            Address(
                kind=AddressType.work,
                street_name=None,  # type: ignore
                pincode=560001,
                country='India'
            )

        with self.assertRaises(ValueError):
            Address(
                kind=AddressType.work,
                street_name='Microservices Ave',
                pincode=None,  # type: ignore
                country='India'
            )

        with self.assertRaises(ValueError):
            Address(
                kind=AddressType.work,
                street_name='Microservices Ave',
                pincode=560001,
                country=None  # type: ignore
            )

        addr = Address(
            kind=AddressType.work,
            street_name='Microservices Ave',
            pincode=560001,
            country='India'
        )

        with self.assertRaises(ValueError):
            addr.kind = None  # type: ignore

        with self.assertRaises(ValueError):
            addr.street_name = None  # type: ignore

        with self.assertRaises(ValueError):
            addr.pincode = None  # type: ignore

        with self.assertRaises(ValueError):
            addr.country = None  # type: ignore

        with self.assertRaises(ValueError):
            Phone(
                kind=None,  # type: ignore
                country_code=1,
                area_code=234,
                local_number=5678900
            )

        with self.assertRaises(ValueError):
            Phone(
                kind=AddressType.work,
                country_code=None,  # type: ignore
                area_code=234,
                local_number=5678900
            )

        with self.assertRaises(ValueError):
            Phone(
                kind=AddressType.work,
                country_code=1,
                area_code=234,
                local_number=None  # type: ignore
            )

        p = Phone(
            kind=AddressType.work,
            country_code=1,
            area_code=234,
            local_number=5678900
        )

        with self.assertRaises(ValueError):
            p.kind = None  # type: ignore

        with self.assertRaises(ValueError):
            p.country_code = None  # type: ignore

        with self.assertRaises(ValueError):
            p.local_number = None  # type: ignore

        with self.assertRaises(ValueError):
            Email(
                kind=None,  # type: ignore
                email='datamodel@microservices.py'
            )

        with self.assertRaises(ValueError):
            Email(
                kind=AddressType.work,
                email=None  # type: ignore
            )

        e = Email(
            kind=AddressType.work,
            email='datamodel@microservices.py'
        )

        with self.assertRaises(ValueError):
            e.kind = None  # type: ignore

        with self.assertRaises(ValueError):
            e.email = None  # type: ignore

        with self.assertRaises(ValueError):
            AddressEntry(full_name=None)  # type: ignore

        a = AddressEntry(full_name='abc')

        with self.assertRaises(ValueError):
            a.full_name = None  # type: ignore


if __name__ == '__main__':
    unittest.main()
