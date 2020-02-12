import bs4
import requests
import collections


class Fodmap:
    def __init__(self):
        self.__resp = requests.get("https://livinghappywithibs.com/tag/printable-fodmap-food-list/")
        self.__resp.raise_for_status()
        self.__soup = bs4.BeautifulSoup(self.__resp.text, 'html.parser')
        self.__lowFodmap = []
        self.__highFodmap = []

    def get_low_fodmap(self):
        for item in self.__soup.find(id='post-63').findAll('ul'):
            for food in item.find_all('li'):
                if '<li>' in str(food) and "href" not in str(food):
                    self.__lowFodmap.append(food.get_text())
        return self.__lowFodmap

    def get_high_fodmap(self):
        for item in self.__soup.find(id='post-41').findAll('ul'):
            for food in item.find_all('li'):
                if '<li>' in str(food) and "href" not in str(food):
                    self.__highFodmap.append(food.get_text())
        return self.__highFodmap

    def fodmap_tuple_list(self):
        fodmap_list = []
        low = self.get_low_fodmap()
        high = self.get_high_fodmap()
        fodmap_diet = collections.namedtuple("fodmap_diet", "Name , Status")
        for food in low:
            fodmap_list.append(fodmap_diet(food,"Low"))
        for food in high:
            fodmap_list.append(fodmap_diet(food,"High"))
        return fodmap_list


if __name__ == "__main__":
    fodmap = Fodmap()
    low_fodmap = fodmap.get_low_fodmap()
    high_fodmap = fodmap.get_high_fodmap()
    fodmap_list = fodmap.fodmap_tuple_list()
    print(fodmap_list)