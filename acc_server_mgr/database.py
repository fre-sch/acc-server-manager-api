import peewee

# db = peewee.DatabaseProxy()
db = peewee.SqliteDatabase("./app.db", pragmas={
    "journal_mode": "wal",
    "cache_size": -1 * 64000,
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0
})
# db.initialize(sqlite_db)


class Base(peewee.Model):
    class Meta:
        database = db


def use_db():
    return db
