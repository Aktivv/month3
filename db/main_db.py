import sqlite3
from db import queries

db = sqlite3.connect('db/online_store.sqlite3')
cur = db.cursor()


async def sql_create():
    if db:
        cur.execute(queries.CREATE_TABLE_STORE)
        print('База данных подключена')
    db.commit()


async def sql_insert_store(name, article, size, count, price, photo):
    cur.execute(queries.INSERT_STORE, (
        name,
        article,
        size,
        count,
        price,
        photo))
db.commit()
