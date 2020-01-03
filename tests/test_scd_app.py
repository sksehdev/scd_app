import requests
import pytest

URL = 'http://0.0.0.0:5000/'


def test_status_code():
    assert requests.get(URL).status_code == 200


@pytest.mark.parametrize("arg, ret", [
    ('Almonds', 'Legal'),
    ('Wine', 'Legal'),
    ('agar-agar', 'Illegal'),
    ("baker's yeast", 'Illegal'),
    ('orange juice', 'Legal'),
    ('cumin', "Food is not in list"),
    ('$$$', "Please enter a valid food item"),
    ('333', "Please enter a valid food item")
])
def test_food_status(arg, ret):
    resp = requests.get(f'{URL}food/items/{arg}')
    assert resp.json()['Status'] == ret


