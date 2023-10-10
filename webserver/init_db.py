"""Initialise a database with generated dummy data"""

import sqlite3
from pathlib import Path

import database

root_dir = Path(__file__).parents[1]
print(root_dir)

db_path = Path.joinpath(root_dir, "db", "database.db")
connection = sqlite3.connect(db_path)


schema_path = Path.joinpath(root_dir, "db", "schema.sql")
print(schema_path)
with open(schema_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

test_moisture_path = Path.joinpath(root_dir, "misc", "src", "data", "test_moisture.txt")
with open(test_moisture_path, 'r') as f:
    lines = f.readlines()

    # skip the header line
    for line in lines[1:]:
        separated = line.strip().split(",")
        print(separated)

        database.insert_moisture_record(f"{separated[0]}", separated[1], f"{separated[2]}", separated[3])


connection.commit()
connection.close()