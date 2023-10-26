from yoyo import step
__depends__ = {}

steps = [
    step("""
    CREATE TABLE IF NOT EXISTS client(
    uuid UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    expiration INTEGER,
    request_limit INTEGER
    );
    """, 
    "DROP TABLE IF EXISTS client")
]
