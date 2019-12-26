from flask import Flask, jsonify, request, render_template
import json


app = Flask(__name__)

USER_LEGAL_LIST = []
USER_ILLEGAL_LIST = []


def load_scd_list():
    with open('data.json') as file:
        scd_dict = json.load(file)
    scd_list = [json.loads(item) for item in scd_dict]
    return scd_list


def create_legal_list():
    scd_list = load_scd_list()
    return [item["Name"].lower() for item in scd_list if item["Status"] == "Legal"]


def create_illegal_list():
    scd_list = load_scd_list()
    return [item["Name"].lower() for item in scd_list if item["Status"] == "Illegal"]


def print_list():
    scd_list = load_scd_list()
    scd_list_str = ''
    for item in scd_list:
        scd_list_str += f'{item["Name"]} has status {item["Status"]} \n'
    return scd_list_str

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/")
# def index():
#     return "Hello World!"

@app.route("/food/items/")
def print_scd_list():
    scd_list_str = print_list()
    return scd_list_str

@app.route("/food/items/lists/")
def print_legal_illegal_list():
    return jsonify({"Lists": {"Legal List ": create_legal_list(), "Illegal List ": create_illegal_list()}})


@app.route("/food/addToUserList", methods=["POST"])
def addfoodtouserlist():
    request_data = request.get_json()
    print(request_data)
    food_item = request_data["Food"]
    food_status = request_data["Status"]
    if food_status == "Legal":
        USER_LEGAL_LIST.append(food_item)
        return jsonify({"User Legal List ": USER_LEGAL_LIST})
    if food_status == "IlLegal":
        USER_ILLEGAL_LIST.append(food_item)
        return jsonify({"User IlLegal List ": USER_ILLEGAL_LIST})



@app.route("/food/items/<string:name>")
def get_status(name):
    legal_list = create_legal_list()
    illegal_list = create_illegal_list()
    if name.lower() not in legal_list and name.lower() not in illegal_list:
        return jsonify({"Food": name.title(), "Status": "Food not in the list "})
    if name.lower() in legal_list:
        return jsonify({"Food": name.title(), "Status": "Legal"})
    if name.lower() in illegal_list:
        return jsonify({"Food": name.title(), "Status": "Illegal"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # print(print_list())
    # print(create_legal_list())
    # print(create_illegal_list())
