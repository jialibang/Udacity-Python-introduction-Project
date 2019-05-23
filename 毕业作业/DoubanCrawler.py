# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import expanddouban
from bs4 import BeautifulSoup
import csv
import requests
import time
from selenium import webdriver
import codecs

# Task 1————————————————————————————————————————————————————————————
def getMovieUrl(category, location):
    url = None
    url = urljoin("https://movie.douban.com/", "tag/#/?sort=S&range=9,10&tags=" + "电影" + "," + category + "," + location)
    return url

# Task 2————————————————————————————————————————————————————————————
def getMoveHtml(url, loadmore=True, waittime=2):
    return expanddouban.getHtml(url, loadmore, waittime)

# Task 3—————————————————————————————————————————————————————————-——
class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

# Task 4  ———————————————————————————————————————————————————————————
def getMovies(category, location):
    soup = BeautifulSoup(getMoveHtml(getMovieUrl(category, location)), "html.parser")
    b = soup.find("div", class_="list-wp")
    moive_list = []
    if b.find("a"):
        for child in b.find_all("a"):
            name = child.find("span", True, class_="title").string
            if child.find("span", True, class_="rate").string :
                rate = float(child.find("span", True, class_="rate").string)
            else:
                rate = 9.0
            location = location
            category = category
            info_link = child['href']
            cover_link = child.find("span", True).img['src']
            time.sleep(2)
            moive_list.append(Movie(name, rate, location, category, info_link, cover_link))
        return moive_list


# Task 5 helper function ———————————————————————————————————————————————————
def getLocList(url="https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影"):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    time.sleep(2)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    loc_list = []

    b = soup.body.find("span", class_="tag-checked tag", text="全部地区").find_parent()
    for sibling in b.next_siblings:
        loc_list.append(sibling.string)
    return loc_list


def makeMovieList(category1="剧情", category2="爱情", category3="喜剧"):
    cate_list = [category1, category2, category3]
    loc_list = getLocList()
    movie_list = []
    for element1 in cate_list:
        for element2 in loc_list:
            get_list = getMovies(element1, element2)
            if get_list:
                for item in get_list:
                    movie_list.append(item)
                    time.sleep(2)
            else:
                break
    return movie_list

def makeListCsv(moive_list):
    with codecs.open("movies.csv", "w", 'utf_8_sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for item in moive_list:
            writer.writerow([item.name, item.rate, item.location, item.category, item.info_link, item.cover_link])
# Task 5————————————————————————————————————————————————————————————
makeListCsv(makeMovieList())

# # Task 6 helper functions———————————————————————————————————————————————————
def makeCsvList():
    with open("movies.csv", "r", encoding="utf-8", newline='') as csv_file:
        movies_list = []
        all_lines = csv.reader(csv_file)
        for line in all_lines:
            movies_list.append(line)
        return movies_list


def getCsvCategory(movies_list):
    category_set = set()
    category_list =[]
    for list in movies_list:
        category_set.add(list[3])
    while len(category_set) != 0:
        category_list.append(category_set.pop())
    return category_list


def get3KindsList(movie_list, category_list):
    list_of_ca0 = []
    list_of_ca1 = []
    list_of_ca2 = []
    for list in movie_list:
        if list[3] == category_list[0]:
            list_of_ca0.append(list)
        elif list[3] == category_list[1]:
            list_of_ca1.append(list)
        elif list[3] == category_list[2]:
            list_of_ca2.append(list)
    return [list_of_ca0, list_of_ca1, list_of_ca2]


def getDicOf_L_N(list_of_ca):
    dic_of_L_N={}
    for list in list_of_ca:
        if list[2] in dic_of_L_N:
            dic_of_L_N[list[2]] += 1
        else:
            dic_of_L_N[list[2]] = 1
    return dic_of_L_N

def getMax3listOf_L_N(dic_of_L_N):
    down_list = sorted(dic_of_L_N.items(), key=lambda item: item[1], reverse=True)
    return down_list[:3]

# Task 6 ———————————————————————————————————————————————————————————
category_list = getCsvCategory(makeCsvList())
cat_of_3_lists = get3KindsList(makeCsvList(), category_list)
with open("output.txt", "w", encoding="utf-8") as f:
    i = 0
    while i < 3:
        out_txt = "{}电影类型中电影总数量{}；该电影类型中数量排名前三的地区分别为{}、{}、{}；该地区电影数量占该类型电影数量比例分别" \
                  "{}、{}、{}。\n".format(category_list[i], len(cat_of_3_lists[i]), getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[0][0],
                                    getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[1][0], getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[2][0],
                                    "{}%".format(round(100 * getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[0][1] / len(cat_of_3_lists[i]), 2)),
                                    "{}%".format(round(100 * getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[1][1] / len(cat_of_3_lists[i]), 2)),
                                    "{}%".format(round(100 * getMax3listOf_L_N(getDicOf_L_N(cat_of_3_lists[i]))[2][1] / len(cat_of_3_lists[i]), 2)))
        f.writelines(out_txt)
        i += 1
