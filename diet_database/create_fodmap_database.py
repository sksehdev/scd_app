import sqlite3
import json
from typing import List
from contextlib import contextmanager
import sys
sys.path.insert(0,"/Users/sandeep/PycharmProjects/Food_app/SCD_APP/")
from diet_scrapper import low_fodmap



@contextmanager
def create_db():
    try:
        conn = sqlite3.connect("fodmap_db.db")
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.close()


def create_table():
    with create_db() as cursor:
        cursor.execute("CREATE TABLE FODMAP_LIST (Food TEXT , Status TEXT)")
    print('fodmap_db.db has been created')


def load_fodmap_list() -> List:
    with open('fodmap_list.json') as file:
        scd_dict = json.load(file)
    scd_list = [json.loads(item) for item in scd_dict]
    return scd_list

def populatedb(data):
    with sqlite3.connect("fodmap_db.db") as connection:
          cursor = connection.cursor()
          for food in data:
              cursor.execute("INSERT INTO FODMAP_LIST VALUES(? ,?)", [food.Name.lower(), food.Status])


if __name__ == "__main__":
    fodmap = low_fodmap.Fodmap()
    fodmap_list = fodmap.fodmap_tuple_list()
    #print(fodmap_list)
    create_db()
    create_table()
    populatedb(fodmap_list)