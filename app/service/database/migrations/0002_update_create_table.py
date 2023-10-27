from yoyo import step
__depends__ = {"0001__define_tables"}

steps = [
    step("""
    ALTER TABLE client
    ADD COLUMN test INTEGER;
    """,
         "ALTER TABLE client DROP COLUMN test"),

    step("""
    CREATE TABLE IF NOT EXISTS testing(
    uuid UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    expiration INTEGER,
    request_limit INTEGER,
    test INTEGER,
    fk UUID REFERENCES client(uuid)
    );
    """,
         "DROP TABLE IF EXISTS testing")
]
