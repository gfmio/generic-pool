from queue import Full

import pytest

from generic_pool import Factory, Pool, UnableToCreateValidObject


class MyObject:
    pass


class MyObjectFactory(Factory):
    def create(self):
        return MyObject()


class InvalidMyObjectFactory(MyObjectFactory):
    def validate(self, item: MyObject) -> bool:
        return False


@pytest.fixture
def factory():
    return MyObjectFactory()


@pytest.fixture
def invalid_factory():
    return InvalidMyObjectFactory()


@pytest.fixture
def pool(factory):
    return Pool(factory)


@pytest.fixture
def invalid_pool(invalid_factory):
    return Pool(invalid_factory)


@pytest.fixture
def three_item_pool(factory):
    return Pool(factory, maxsize=3)


def test_pool_acquire_release(pool: Pool):
    item = pool.acquire()
    assert isinstance(item, MyObject)
    assert len(pool._items) == 1
    assert pool._available_items.empty()
    pool.release(item)
    assert len(pool._items) == 1
    assert pool._available_items.qsize() == 1


def test_pool_with_item(pool: Pool):
    with pool.item() as item:
        assert isinstance(item, MyObject)
        assert len(pool._items) == 1
        assert pool._available_items.empty()
    assert len(pool._items) == 1
    assert pool._available_items.qsize() == 1


def test_invalid_pool(invalid_pool: Pool):
    with pytest.raises(UnableToCreateValidObject):
        invalid_pool.acquire()


def test_limited_size(three_item_pool: Pool):
    with pytest.raises(Full):
        with three_item_pool.item():
            with three_item_pool.item():
                with three_item_pool.item():
                    with three_item_pool.item():
                        pass
