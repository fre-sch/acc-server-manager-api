# Storage module implementation

Storage module implementation must provide functions:


```python
def create_one(db: peewee.Database,
               data: "instance of pydantic model"
               ) -> "instance of peewee model":
    """
    `data` is pre-validated by corresponding controller.
    """
    pass
```

```python
def get_one(db: peewee.Database, _id: int
            ) -> Optional["instance of peewee model"]:
    """
    Return None on missing row  for `_id`, controller must "none-check" to raise
    not found.
    """
    pass
```

```python
def update_one(db: peewee.Database, _id: int,
               data: "instance of pydantic model"
               ) -> Optional["instance of peewee model"]:
    """
    `data` is prevalidated by corresponding controller.
    Do not raise on missing row for _id, return None instead, controller must
    none-check to raise not found.
    """
    pass
```

```python
def delete_one(db: peewee.Database, _id: int):
    """
    Do not raise on missing database record for `_id`. Has no return value.
    Attempting delete for non-existing `_id` results in intended outcome:
    record for `_id` doesn't exist.
    """
    pass
```

```python
def search(db: peewee.Database, filter_: FilterRequest
           ) -> tuple[int, list["instance of peewee model"]]:
    """
    Returns a tuple with total count of database rows matching `filter_` and
    list containing matching rows offset, limited, sorted by `filter_`.
    """
    pass
```

Additional functions should follow this general pattern, must at least have
first positional parameter ``db: peewee.Database``.
