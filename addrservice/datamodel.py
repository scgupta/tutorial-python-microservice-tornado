# Copyright (c) 2020. All rights reserved.

from enum import Enum, unique
from typing import (
    Any,
    Mapping,
    Optional,
    Sequence,
    Union
)


VALUE_ERR_MSG = '{} has invalid value {}'


@unique
class AddressType(Enum):
    home = 1,
    work = 2


class Address:
    def __init__(
        self,
        kind: AddressType,
        street_name: str,
        pincode: Union[int, str],
        country: str,
        building_name: str = None,
        unit_number: int = None,
        street_number: Union[int, str] = None,
        locality: str = None,
        city: str = None,
        province: str = None,
    ):
        if kind is None:
            raise ValueError(VALUE_ERR_MSG.format('kind', kind))
        if not street_name:
            raise ValueError(VALUE_ERR_MSG.format('street_name', street_name))
        if not pincode:
            raise ValueError(VALUE_ERR_MSG.format('pincode', pincode))
        if not country:
            raise ValueError(VALUE_ERR_MSG.format('country', country))

        self._kind = kind
        self._building_name = building_name
        self._unit_number = unit_number
        self._street_number = street_number
        self._street_name = street_name
        self._locality = locality
        self._city = city
        self._province = province
        self._pincode = pincode
        self._country = country

    @classmethod
    def from_api_dm(cls, vars: Mapping[str, Any]) -> 'Address':
        return Address(
            kind=AddressType[vars['kind']],
            street_name=vars['street_name'],
            pincode=vars['pincode'],
            country=vars['country'],
            building_name=vars.get('building_name'),
            unit_number=vars.get('unit_number'),
            street_number=vars.get('street_number'),
            locality=vars.get('locality'),
            city=vars.get('city'),
            province=vars.get('province'),
        )

    @property
    def kind(self) -> AddressType:
        return self._kind

    @kind.setter
    def kind(self, value: AddressType) -> None:
        if value is None:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._kind = value

    @property
    def building_name(self) -> Optional[str]:
        return self._building_name

    @building_name.setter
    def building_name(self, value: str) -> None:
        self._building_name = value

    @property
    def unit_number(self) -> Optional[int]:
        return self._unit_number

    @unit_number.setter
    def unit_number(self, value: int) -> None:
        self._unit_number = value

    @property
    def street_number(self) -> Optional[Union[int, str]]:
        return self._street_number

    @street_number.setter
    def street_number(self, value: Union[int, str]) -> None:
        self._street_number = value

    @property
    def street_name(self) -> str:
        return self._street_name

    @street_name.setter
    def street_name(self, value: str) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._street_name = value

    @property
    def locality(self) -> Optional[str]:
        return self._locality

    @locality.setter
    def locality(self, value: str) -> None:
        self._locality = value

    @property
    def city(self) -> Optional[str]:
        return self._city

    @city.setter
    def city(self, value: str) -> None:
        self._ = value

    @property
    def province(self) -> Optional[str]:
        return self._province

    @province.setter
    def province(self, value: str) -> None:
        self._province = value

    @property
    def pincode(self) -> Union[int, str]:
        return self._pincode

    @pincode.setter
    def pincode(self, value: Union[int, str]) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._pincode = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._country = value

    def to_api_dm(self) -> Mapping[str, Any]:
        d = {
            'kind': self.kind.name,
            'building_name': self.building_name,
            'unit_number': self.unit_number,
            'street_number': self.street_number,
            'street_name': self.street_name,
            'locality': self.locality,
            'city': self.city,
            'province': self.province,
            'pincode': self.pincode,
            'country': self.country,
        }

        return {k: v for k, v in d.items() if v is not None}


class Phone:
    def __init__(
        self,
        kind: AddressType,
        country_code: int,
        local_number: int,
        area_code: int = None,
    ):
        if kind is None:
            raise ValueError(VALUE_ERR_MSG.format('kind', kind))
        if not country_code:
            raise ValueError(VALUE_ERR_MSG.format(
                'country_code',
                country_code
            ))
        if not local_number:
            raise ValueError(VALUE_ERR_MSG.format(
                'local_number',
                local_number
            ))

        self._kind = kind
        self._country_code = country_code
        self._area_code = area_code
        self._local_number = local_number

    @classmethod
    def from_api_dm(cls, vars: Mapping[str, Any]) -> 'Phone':
        return Phone(
            kind=AddressType[vars['kind']],
            country_code=vars['country_code'],
            local_number=vars['local_number'],
            area_code=vars.get('area_code'),
        )

    @property
    def kind(self) -> AddressType:
        return self._kind

    @kind.setter
    def kind(self, value: AddressType) -> None:
        if value is None:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._kind = value

    @property
    def country_code(self) -> int:
        return self._country_code

    @country_code.setter
    def country_code(self, value: int) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._country_code = value

    @property
    def area_code(self) -> Optional[int]:
        return self._area_code

    @area_code.setter
    def area_code(self, value: int) -> None:
        self._ = value

    @property
    def local_number(self) -> int:
        return self._local_number

    @local_number.setter
    def local_number(self, value: int) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._local_number = value

    def to_api_dm(self) -> Mapping[str, Any]:
        d = {
            'kind': self.kind.name,
            'country_code': self.country_code,
            'area_code': self.area_code,
            'local_number': self.local_number,
        }

        return {k: v for k, v in d.items() if v is not None}


class Email:
    def __init__(
        self,
        kind: AddressType,
        email: str,
    ):
        if kind is None:
            raise ValueError(VALUE_ERR_MSG.format('kind', kind))
        if not email:
            raise ValueError(VALUE_ERR_MSG.format('value', email))

        self._kind = kind
        self._email = email

    @classmethod
    def from_api_dm(cls, vars: Mapping[str, Any]) -> 'Email':
        return Email(
            kind=AddressType[vars['kind']],
            email=vars['email'],
        )

    @property
    def kind(self) -> AddressType:
        return self._kind

    @kind.setter
    def kind(self, value: AddressType) -> None:
        if value is None:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._kind = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('value', value))

        self._email = value

    def to_api_dm(self) -> Mapping[str, Any]:
        d = {
            'kind': self.kind.name,
            'email': self.email,
        }

        return {k: v for k, v in d.items() if v is not None}


class AddressEntry:
    def __init__(
        self,
        full_name: str,
        addresses: Sequence[Address] = [],
        phone_numbers: Sequence[Phone] = [],
        fax_numbers: Sequence[Phone] = [],
        emails: Sequence[Email] = [],
    ):
        if not full_name:
            raise ValueError(VALUE_ERR_MSG.format('full_name', full_name))

        self._full_name = full_name
        self._addresses = list(addresses)
        self._phone_numbers = list(phone_numbers)
        self._fax_numbers = list(fax_numbers)
        self._emails = list(emails)

    @classmethod
    def from_api_dm(cls, vars: Mapping[str, Any]) -> 'AddressEntry':
        return AddressEntry(
            full_name=vars['full_name'],
            addresses=[
                Address.from_api_dm(x) for x in vars.get('addresses', [])
            ],
            phone_numbers=[
                Phone.from_api_dm(x) for x in vars.get('phone_numbers', [])
            ],
            fax_numbers=[
                Phone.from_api_dm(x) for x in vars.get('fax_numbers', [])
            ],
            emails=[
                Email.from_api_dm(x) for x in vars.get('emails', [])
            ],
        )

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value:
            raise ValueError(VALUE_ERR_MSG.format('full_name', value))

        self._full_name = value

    @property
    def addresses(self) -> Sequence[Address]:
        return self._addresses

    @addresses.setter
    def addresses(self, value: Sequence[Address]) -> None:
        self._addresses = list(value)

    @property
    def phone_numbers(self) -> Sequence[Phone]:
        return self._phone_numbers

    @phone_numbers.setter
    def phone_numbers(self, value: Sequence[Phone]) -> None:
        self._phone_numbers = list(value)

    @property
    def fax_numbers(self) -> Sequence[Phone]:
        return self._fax_numbers

    @fax_numbers.setter
    def fax_numbers(self, value: Sequence[Phone]) -> None:
        self._fax_numbers = list(value)

    @property
    def emails(self) -> Sequence[Email]:
        return self._emails

    @emails.setter
    def emails(self, value: Sequence[Email]) -> None:
        self._emails = list(value)

    def to_api_dm(self) -> Mapping[str, Any]:
        d = {
            'full_name': self.full_name,
            'addresses': [x.to_api_dm() for x in self.addresses],
            'phone_numbers': [x.to_api_dm() for x in self.phone_numbers],
            'fax_numbers': [x.to_api_dm() for x in self.fax_numbers],
            'emails': [x.to_api_dm() for x in self.emails],
        }

        return {k: v for k, v in d.items() if v is not None}
