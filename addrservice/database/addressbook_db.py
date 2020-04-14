# Copyright (c) 2020. All rights reserved.

from abc import ABCMeta, abstractmethod
import aiofiles  # type: ignore
import json
import os
from typing import AsyncIterator, Dict, Mapping, Tuple
import uuid

from addrservice.datamodel import AddressEntry


class AbstractAddressBookDB(metaclass=ABCMeta):
    def start(self):
        pass

    def stop(self):
        pass

    # CRUD

    @abstractmethod
    async def create_address(
        self,
        addr: AddressEntry,
        nickname: str = None
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def read_address(self, nickname: str) -> AddressEntry:
        raise NotImplementedError()

    @abstractmethod
    async def update_address(self, nickname: str, addr: AddressEntry) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_address(self, nickname: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def read_all_addresses(self) -> AsyncIterator[Tuple[str, AddressEntry]]:
        raise NotImplementedError()


class InMemoryAddressBookDB(AbstractAddressBookDB):
    def __init__(self):
        self.db: Dict[str, AddressEntry] = {}

    async def create_address(
        self,
        addr: AddressEntry,
        nickname: str = None
    ) -> str:
        if nickname is None:
            nickname = uuid.uuid4().hex

        if nickname in self.db:
            raise KeyError('{} already exists'.format(nickname))

        self.db[nickname] = addr
        return nickname

    async def read_address(self, nickname: str) -> AddressEntry:
        return self.db[nickname]

    async def update_address(self, nickname: str, addr: AddressEntry) -> None:
        if nickname is None or nickname not in self.db:
            raise KeyError('{} does not exist'.format(nickname))

        self.db[nickname] = addr

    async def delete_address(self, nickname: str) -> None:
        if nickname is None or nickname not in self.db:
            raise KeyError('{} does not exist'.format(nickname))

        del self.db[nickname]

    async def read_all_addresses(
        self
    ) -> AsyncIterator[Tuple[str, AddressEntry]]:
        for nickname, addr in self.db.items():
            yield nickname, addr


class FilesystemAddressBookDB(AbstractAddressBookDB):
    def __init__(self, store_dir_path: str):
        store_dir = os.path.abspath(store_dir_path)
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        if not (os.path.isdir(store_dir) and os.access(store_dir, os.W_OK)):
            raise ValueError(
                'String store "{}" is not a writable directory'.format(
                    store_dir
                )
            )
        self._store = store_dir

    @property
    def store(self) -> str:
        return self._store

    def _file_name(self, nickname: str) -> str:
        return os.path.join(
            self.store,
            nickname + '.json'
        )

    def _file_exists(self, nickname: str) -> bool:
        return os.path.exists(self._file_name(nickname))

    async def _file_read(self, nickname: str) -> Dict:
        try:
            async with aiofiles.open(
                self._file_name(nickname),
                encoding='utf-8',
                mode='r'
            ) as f:
                contents = await f.read()
                return json.loads(contents)
        except FileNotFoundError:
            raise KeyError(nickname)

    async def _file_write(self, nickname: str, addr: Mapping) -> None:
        async with aiofiles.open(
            self._file_name(nickname),
            mode='w',
            encoding='utf-8'
        ) as f:
            await f.write(json.dumps(addr))

    async def _file_delete(self, nickname: str) -> None:
        os.remove(self._file_name(nickname))

    async def _file_read_all(self) -> AsyncIterator[Tuple[str, Dict]]:
        all_files = os.listdir(self.store)
        extn_end = '.json'
        extn_len = len(extn_end)
        for f in all_files:
            if f.endswith(extn_end):
                nickname = f[:-extn_len]
                addr = await self._file_read(nickname)
                yield nickname, addr

    async def create_address(
        self,
        addr: AddressEntry,
        nickname: str = None
    ) -> str:
        if nickname is None:
            nickname = uuid.uuid4().hex

        if self._file_exists(nickname):
            raise KeyError('{} already exists'.format(nickname))

        await self._file_write(nickname, addr.to_api_dm())
        return nickname

    async def read_address(self, nickname: str) -> AddressEntry:
        addr = await self._file_read(nickname)
        return AddressEntry.from_api_dm(addr)

    async def update_address(self, nickname: str, addr: AddressEntry) -> None:
        if self._file_exists(nickname):
            await self._file_write(nickname, addr.to_api_dm())
        else:
            raise KeyError(nickname)

    async def delete_address(self, nickname: str) -> None:
        if self._file_exists(nickname):
            await self._file_delete(nickname)
        else:
            raise KeyError(nickname)

    async def read_all_addresses(
        self
    ) -> AsyncIterator[Tuple[str, AddressEntry]]:
        async for nickname, addr in self._file_read_all():
            yield nickname, AddressEntry.from_api_dm(addr)
