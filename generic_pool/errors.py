from typing import Generic, TypeVar

T = TypeVar("T")


class Invalid(Exception, Generic[T]):
    def __init__(self, item: T):
        super()
        self.message = "Invalid object"
        self.item = item


class UnableToCreateValidObject(Exception, Generic[T]):
    def __init__(self):
        super()
        self.message = "Unable to create a valid object"


class Unmanaged(Exception, Generic[T]):
    def __init__(self, item: T):
        super()
        self.message = "Unmanaged object"
        self.item = item
