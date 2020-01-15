import bs4
import requests
import collections
import string
from typing import List
import json

json_file = 'scd_list.json'


def list_of_foods() -> List:
    alpha = list(string.ascii_uppercase)
    scd_items = []
    scd_diet = collections.namedtuple("scd_diet", "Name , Status")
    for letter in alpha:
        resp = requests.get(f"http://www.breakingtheviciouscycle.info/legal/listing/{letter}/")
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        for item in soup.find(id="btvc_tbl_listing").find_all("tr"):
            scd_items.append(scd_diet(item.find_all("td")[0].get_text().rstrip(), item.find_all("td")[1].get_text()))
    return scd_items


def write_list_to_json(scd_list: list):
   dict_list = []
   for item in scd_list:
        dict_list.append(json.dumps(item._asdict()))
   with open(json_file, 'w', encoding='utf-8') as f:
         json.dump(dict_list, f, ensure_ascii=False, indent=4)


def load_scd_list() -> List:
    scd_list_tuple = []
    scd_diet = collections.namedtuple("scd_diet", "Name , Status")
    with open('scd_list.json') as file:
        scd_dict = json.load(file)
    for item in scd_dict:
        scd_list_tuple.append(scd_diet(**json.loads(item)))
    return scd_list_tuple


def food_status(scd_list: list):
    food = input("Please enter the food : ")
    scd_legal_items = [item.Name for item in scd_list if item.Status == "Legal"]
    scd_illegal_items = [item.Name for item in scd_list if item.Status == "Illegal"]
    if food in scd_illegal_items:
        print(f'{food} is Illegal')
    elif food in scd_legal_items:
        print(f'{food} is Legal')
    else:
        print(f'{food} is not present in SCD list')


if __name__ == "__main__":
    reload = input("Do you want to reload the list from SCD website? Reply Y to reload : ")
    if reload == "Y":
        scd_list_reload = list_of_foods()
        write_list_to_json(scd_list_reload)
    while True:
        cached_scd_list = load_scd_list()
        food_status(cached_scd_list)
