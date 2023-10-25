
from yoyo import read_migrations
from yoyo import get_backend
from app.Utils import database_url
import os
from typing import List

def find_migrations_dirs() -> List[str]:
    root_dir = os.getcwd()
    found_paths = list()
    for root, dirs, _ in os.walk(root_dir):
        if "migrations" in dirs and "python" not in root:
            print(root)
            found_paths.append(os.path.join(root, "migrations"))
    return found_paths


def apply_migrations(database_uri, migrations_path):
    backend = get_backend(database_uri)
    migrations = read_migrations(migrations_path)

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))


def run():
    # Check if the migrations directory exists
    migrations_dirs = find_migrations_dirs()
    try:
        # Apply migrations if the directory exists
        for migration_path in migrations_dirs:
            apply_migrations(database_url, migration_path)
    except Exception as e:
        raise Exception(f"Couldn't apply the migrations, {e}")
