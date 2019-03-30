import requests
import re
import time
from bs4 import BeautifulSoup
import jieba
import wordcloud
import numpy as np
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
# 'https://movie.douban.com/subject/11537954/episode/2/?discussion_start=30#comment-section'
def getpage(url):
    res=requests.get(url)
    html=res.text
    soup = BeautifulSoup(html,"html.parser")
    comments_sec = soup.find_all(class_="bd")
    for i in comments_sec:
        comments_list = i.find_all("span")
        if len(comments_list)>3:
            return comments_list[1].text

def getpages(id,num):
    data =""
    for i in range(id):
        for j in range(num):
            url = "https://movie.douban.com/subject/11537954/episode/" + str(i+1) + "/?discussion_start=" + str(10 * j) + "#comment-section"
            resp=getpage(url)
            if resp==None:
                continue
            data += resp
            print(data)
            print("parsing page %d" % (j+ 1))
            time.sleep(6)  # 每隔6秒爬取一页，豆瓣默认5秒，太频繁了不好哦
    print(data)
    return data

if __name__=='__main__':
    data = getpages(10,6)  # 10为要爬取的页数
    all_comments = jieba.lcut(data)
    words = " ".join(all_comments)
    print("正在生成词云图……")
    backgroud_Image = np.array(Image.open('pigs.jpg'))
    wc = wordcloud.WordCloud(width=900, height=900,mask=backgroud_Image,background_color='white', font_path='hk.ttf')
    wc.generate_from_text(words)
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)
    wc.to_file("images.jpg")
    print("ok")
