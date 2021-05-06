from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Factory(ABC, Generic[T]):
    """Provides methods for creating, validating and releasing `T` objects and managed resources"""

    @abstractmethod
    def create(self) -> T:
        """Create a new `T` object and allocates relevant resources"""
        ...

    def validate(self, item: T) -> bool:
        """Check if `item` is valid"""
        return True

    def destroy(self, item: T) -> None:
        """Release resources managed by the `T` object"""
        return True
