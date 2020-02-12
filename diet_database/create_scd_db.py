import sqlite3
import json
from typing import List
from contextlib import contextmanager



@contextmanager
def create_db():
    try:
        conn = sqlite3.connect("scd_list_db.db")
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.close()


def create_table():
    with create_db() as cursor:
        cursor.execute("CREATE TABLE SCD_LIST (Food TEXT , Status TEXT)")
    print('scd_list_db.db has been created')


def load_scd_list() -> List:
    with open('scd_list.json') as file:
        scd_dict = json.load(file)
    scd_list = [json.loads(item) for item in scd_dict]
    return scd_list

def populatedb(data):
    with sqlite3.connect("scd_list_db.db") as connection:
          cursor = connection.cursor()
          for food in data:
              cursor.execute("INSERT INTO SCD_LIST  VALUES(? ,?)", [food["Name"].lower(), food["Status"]])


if __name__ == "__main__":
    create_db()
    #create_table()
    scd_list = load_scd_list()
    print(scd_list)
    populatedb(scd_list)