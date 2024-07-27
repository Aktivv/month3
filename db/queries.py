CREATE_TABLE_STORE = '''
    CREATE TABLE IF NOT EXISTS online_store
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    article INTEGER,
    size VARCHAR(255),
    count INTEGER,
    price FLOAT,
    photo TEXT
    )
'''

INSERT_STORE = '''
    INSERT INTO online_store(name, article, size, count, price, photo)
    VALUES (?, ?, ?, ?, ?, ?)
'''
