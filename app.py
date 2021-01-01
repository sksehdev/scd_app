from flask import Flask, jsonify, request, render_template
import sqlite3
import re
import sys
from contextlib import contextmanager

app = Flask(__name__)

SCD_DB = 'diet_database/scd_list_db.db'
FODMAP_DB = 'diet_database/fodmap_db.db'


def first_launch(DB):
    try:
        conn = sqlite3.connect(DB)
    except:
        sys.exit('Error code X')

#Decorator
@contextmanager
def access_db(DB):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.commit()
        conn.close()


def get_data_from_table(foodname, dbname, tablename):
    with access_db(dbname) as cursor:
        query = f'SELECT Status FROM {tablename} WHERE Food=?'
        result = cursor.execute(query, (foodname.lower(),))
        row = result.fetchone()
    return row

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/food/items/<string:name>")
def get_status(name):
    if re.match('[a-zA-Z]', name):
        row = get_data_from_table(name, SCD_DB, "SCD_LIST")
        if row:
            return {"Food": name, "Status": row[0]}
        return {"Status": "Food is not in list"}
    else:
        return {"Status": "Please enter a valid food item"}


def test_db_connection(name, db, tablename):
    with access_db(db) as cursor:
      query = f'SELECT Status FROM {tablename} WHERE Food=?'
      result = cursor.execute(query, (name.lower(),))
      row = result.fetchone()
    if row:
        return {"Food": name, "Status": row[0]}
    return {}



if __name__ == "__main__":
    first_launch(SCD_DB)
    print(test_db_connection("almonds", SCD_DB, 'SCD_LIST'))
    first_launch(FODMAP_DB)
    print(test_db_connection("almonds", FODMAP_DB, 'FODMAP_LIST'))
    app.run(port=5000, host="0.0.0.0")
