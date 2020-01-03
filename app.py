from flask import Flask, jsonify, request, render_template
import sqlite3
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/")
# def index():
#     return "Hello World!"




@app.route("/food/items/<string:name>")
def get_status(name):
    if re.match('[a-zA-Z]', name):
        connection = sqlite3.connect("scd_database/scd_list_db.db")
        cursor = connection.cursor()

        query = "SELECT Status FROM SCD_LIST WHERE Food=?"

        result = cursor.execute(query, (name.lower(),))
        row = result.fetchone()
        if row:
            return {"Food": name, "Status": row[0]}
        return {"Status": "Food is not in list"}
    else:
        return {"Status": "Please enter a valid food item"}


def test_db_connection(name):
    connection = sqlite3.connect("scd_database/scd_list_db.db")
    cursor = connection.cursor()

    query = "SELECT Status FROM SCD_LIST WHERE Food=?"

    result = cursor.execute(query, (name.lower(),))
    row = result.fetchone()
    if row:
        return {"Food": name, "Status": row[0]}
    return {}

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
    # print(print_list())
    # print(create_legal_list())
    # print(create_illegal_list())
    #test_db_connection('almonds')
