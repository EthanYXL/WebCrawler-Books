import requests
import time
from datetime import datetime
import json
import os
from analysis import create_analyze_plot
from login import get_login_cookies
from bs4 import BeautifulSoup

BASE = "rank/"
if not os.path.exists(BASE):
        os.makedirs(BASE)

cookies = get_login_cookies()


def get_html(url, use_cookies=False):
    if use_cookies:
        response = requests.get(url, verify=False, cookies=cookies)
    else:
        response = requests.get(url, verify=False)
    html = BeautifulSoup(response.text)
    return html


def grab_sorts(url, r18=False):
    result = []
    if r18:
        print("限制級")
        intro_page = get_html(url, True)
    else:
        intro_page = get_html(url)

    sort_section = intro_page.find("ul", class_="sort").find_all("li")
    for sort_group in sort_section:
        sort_list = []
        for i in sort_group.find_all("a"):
            sort_list.append(i.text)
        result.append(sort_list)
    return result


def wait(times):
    # times: 總請求次數
    if times % 30 == 0:
        time.sleep(60)
    elif times % 2 == 0:
        time.sleep(10)


rank_page = get_html("https://www.books.com.tw/web/sys_saletopb/books/?attribute=7")
books = rank_page.find("div", class_="mod_a").find_all("li", class_="item")
table = {
    "Rank": [],
    "Title": [],
    "Author": [],
    "Price": [],
    "Link": [],
    "Sorts": []
}

failure = 0
connect_times = 0
start_time = time.time()  # 開始計時
for book in books:
    book_title = book.find("h4")
    book_link = book_title.find("a")["href"]
    book_rank = book.find("strong", class_="no")
    book_author = book.find("ul", class_="msg").find("a")
    book_price = book.find("li", class_="price_a").find_all("b")[-1]
    table["Rank"].append(book_rank.text)
    table["Title"].append(book_title.text)
    table["Price"].append(book_price.text)
    table["Link"].append(book_link)

    # 取得分類
    try:
        table["Sorts"].append(grab_sorts(book_link))
    except AttributeError:
        connect_times = connect_times + 1
        wait(connect_times)
        table["Sorts"].append(grab_sorts(book_link, True))

    try:
        table["Author"].append(book_author.text)
    except AttributeError:
        table["Author"].append("")
    print(book_title.text)

    print("-" * 30)
    connect_times = connect_times + 1
    wait(connect_times)

end_time = time.time()  # 結束計時
sum_time = end_time - start_time
print("總花費", sum_time, "秒")
print("失敗", failure, "筆")

# 建立json檔案
fn = BASE + "/" + datetime.now().strftime("%Y%m%d") + "_7days.json"
f = open(fn, "w", encoding="utf-8")
json.dump(table, f, ensure_ascii=False, indent=4)
f.close()
create_analyze_plot(fn)

