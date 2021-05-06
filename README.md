# generic-pool

generic-pool is a generic object pool for python inspired by the node.js library.

You can use it to build your own resource pools, e.g. to manage file handles, connections or similar.

## Install

Install `generic-pool` from pypi using your favourite package manager.

```sh
# If you use poetry
poetry add generic-pool

# If you use pip
pip install generic-pool
```

## Usage

```py3
from random

from generic_pool import Factory
from generic_pool import Pool

class IntValue:
    def __init__(self):
        self.value = random.rand
    pass

class FortyTwoFactory(Factory):
    def create(self) -> IntValue:
        return IntValue()

    def validate(self, item: IntValue) -> bool:
        return item.value == 42

    def destroy(self):
        # free resources, not applicable here
        pass

factory = FortyTwoFactory()
pool = Pool(factory)

item = pool.acquire()
try:
    assert item.value == 42
finally:
    pool.release(item)

with pool.acquire(item):
    assert item.value == 42
```

## License

[MIT](LICENSE)
