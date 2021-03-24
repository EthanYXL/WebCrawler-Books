import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
import jieba.analyse
from urllib.request import urlretrieve
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

# 設定圖表預設字體、排版
params = {'axes.labelsize': 24,
          'ytick.labelsize': 18,
          'axes.titlesize': 30,
          'figure.subplot.left': 0.2,
          'figure.subplot.right': 0.95,
          'font.sans-serif': 'Microsoft JhengHei'
          }
plt.rcParams.update(params)
pd.set_option('display.max_rows', None)


def create_analyze_plot(jfile):
    with open(jfile, "r", encoding="utf-8") as jf:
        data = json.load(jf)
    df = pd.DataFrame(data)
    df_sort = df["Sorts"]
    df_title = df["Title"].to_list()
    file_name = jfile.split(".")[0]
    create_first_sorts_plot(df_sort, file_name)
    create_last_sorts_plot(df_sort, file_name)
    creat_wordcloud(df_title, file_name)


# 大類
def get_first_sort(sort_list):
    result = []
    for i in sort_list:
        if i[0] not in result:
            result.append(i[0])
    return result


def create_first_sorts_plot(df_sort, file_name):
    df_f_sort = df_sort.apply(get_first_sort)
    f_sorts = df_f_sort.explode().to_frame()
    plt.figure(figsize=(20, 12))
    fig_f = sns.countplot(y=f_sorts["Sorts"], order=f_sorts["Sorts"].value_counts().index)
    plt.title("7日暢銷榜中出現的書籍類型(大類)")
    # 顯示數量值
    for i, v in enumerate(f_sorts.value_counts()):
        fig_f.text(v + 0.5, i + .16, str(v), color='black', fontweight='light', fontsize=18)
    plt.savefig(file_name+"_f.png")
    print("已建立", file_name+"_f.png")


# 小類
def get_last_sort(sort_list):
    result = []
    for i in sort_list:
        result.append(i[-1])
    return result


def create_last_sorts_plot(df_sort, file_name):
    df_l_sort = df_sort.apply(get_last_sort)
    l_sorts = df_l_sort.explode().to_frame()
    index = l_sorts["Sorts"].value_counts().index
    plt.figure(figsize=(20, 30))
    fig_l = sns.countplot(y=l_sorts["Sorts"], order=index)
    plt.title("7日暢銷榜中出現的書籍類型(細類)", fontsize=30)
    for i, v in enumerate(l_sorts.value_counts()):
        fig_l.text(v + 0.2, i + .2, str(v), color='black', fontweight='light', fontsize=18)
    plt.savefig(file_name+"_l.png")
    print("已建立", file_name + "_l.png")

# 文字雲
def creat_wordcloud(df_title, file_name):
    url = "https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big"
    dicname = "dict.txt.big"
    if not os.path.exists(dicname):
        urlretrieve(url, dicname)
    jieba.set_dictionary(dicname)
    kw = jieba.analyse.extract_tags(str(df_title), topK=300)
    print(kw)
    mask_path = "mask.jpg"
    mask = np.array(Image.open(mask_path))
    wc = WordCloud(font_path="./jf-openhuninn-1.0.ttf",
                   background_color="white", max_words=500,
                   mask=mask, collocations=False)
    wc.generate(" ".join(kw))
    color = ImageColorGenerator(mask)
    wc.recolor(color_func=color)
    wc.to_file(file_name +"_wcloud.png")
