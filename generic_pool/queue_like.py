from typing import Optional, Protocol, TypeVar

T = TypeVar("T")


class QueueLike(Protocol[T]):
    """A queue-like object."""

    def __init__(self, maxsize: Optional[int]) -> None:
        ...

    def get(self, block: Optional[bool] = None) -> T:
        """Get an item from the queue."""
        ...

    def put(self, item: T) -> T:
        """Put an item into the queue."""
        ...

    def empty(self) -> bool:
        """Return whether the queue is empty."""
        ...

    def full(self) -> bool:
        """Return whether the queue is full."""
        ...

    def qsize(self) -> int:
        """Return the (approximate) size of the queue"""
        ...


class QueueLikeFactory(Protocol[T]):
    def __call__(self, maxsize: Optional[int] = None) -> QueueLike[T]:
        ...
