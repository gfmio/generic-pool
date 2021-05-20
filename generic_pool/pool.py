from abc import ABC, abstractmethod
from contextlib import contextmanager
from queue import Empty, Full, LifoQueue, Queue
from typing import Callable, Generic, List, Optional, TypeVar

from .errors import Invalid, UnableToCreateValidObject, Unmanaged
from .factory import Factory

T = TypeVar("T")


class Pool(Generic[T]):
    """A managed pool of `T` objects"""

    def __init__(
        self,
        factory: Factory[T],
        queue_cls: Callable[[], Queue] = LifoQueue,
        maxsize: Optional[int] = None,
        eager: bool = False,
    ):
        self._factory = factory
        self._queue_cls = queue_cls
        self.maxsize = maxsize
        self.eager = eager

        self._items: List[T] = []
        self._available_items: Queue[T] = self._queue_cls(maxsize=self.maxsize or 0)

        if self.eager:
            self.fill()

    def acquire(self) -> T:
        """Acquire a new item from the pool"""
        try:
            item = self._available_items.get(block=False)
        except Empty:
            return self._create()

        if item not in self._items:
            raise Unmanaged(item)

        try:
            if not self._factory.validate(item):
                raise Invalid(item)
            return item
        except Invalid:
            self._destroy(item)
            return self.acquire()
        except Exception as e:
            self._destroy(item)
            raise e

    def release(self, item: T) -> None:
        """Release an item back to the pool"""

        if item not in self._items:
            raise Unmanaged(item)

        if self._factory.validate(item):
            self._available_items.put(item)
        else:
            self._destroy(item)

    def empty(self) -> bool:
        """Returns True if there are no items in the pool"""
        return len(self._items) == 0

    def full(self) -> bool:
        return self.maxsize is not None and len(self._items) >= self.maxsize

    def busy(self) -> bool:
        self._available_items.empty()

    def idle(self) -> bool:
        self._available_items.full()

    def drain(self) -> None:
        while not self.empty():
            item = self._available_items.get()
            self._destroy(item)

    def fill(self) -> None:
        if self.maxsize is None:
            return

        while not self.full():
            item = self._create()
            self.release(item)

    @contextmanager
    def item(self):
        item = self.acquire()
        try:
            yield item
        finally:
            self.release(item)

    def _create(self) -> T:
        if self.full():
            raise Full()

        item = self._factory.create()
        self._items.append(item)

        if not self._factory.validate(item):
            self._destroy(item)
            raise UnableToCreateValidObject()

        return item

    def _destroy(self, item: T) -> None:
        if item not in self._items:
            raise Unmanaged(item)

        self._items.remove(item)
        self._factory.destroy(item)
