import requests
from lxml import etree
import time
import random
from fake_agent import useragent_random as random_agent

# ciligou.app的种子搜索链接

class mPage():
    def __init__(self, url):
        self.header = {
            'User-Agent':
            random_agent(),
            'Connection': 'keep - alive'
        }
        req = requests.get(url, headers=self.header, timeout=5)
        selector = etree.HTML(req.text)
        self.magnet = selector.xpath('//a[@id="down-url"]/@href')[0]
        self.title = selector.xpath('//h1[@class="Information_title"]/text()')[0]
        if len(selector.xpath('//div[@class="Information_l_content"]/b[2]/text()')) > 0:
            self.storage = selector.xpath('//div[@class="Information_l_content"]/b[2]/text()')[0]
        else:
            self.storage = None

class SearchCiligou():
    def __init__(self, word, updateItem=None):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Connection': 'keep - alive'
        }
        self.starturl = "https://ciligou.app"
        self.url = "https://ciligou.app/search?word="
        self.search_word = word
        self.search_url = self.url + str(self.search_word)
        print(self.search_url)
        self.item_lists = []
        self.Update = updateItem
        r = None
        try:
            r = requests.get(self.search_url, headers=self.header, timeout=5)
        except Exception:
            print("connection to ciligou.app web is failed.")
            if self.Update is not None:
                self.Update(None)
        
        webtext = r.text
        selector = etree.HTML(webtext)
        lists = selector.xpath('//ul[@id="Search_list_wrapper"]/li')
        for list in lists:
            print(list.xpath('div[1]/div/a/@href')[0])
            print(list.xpath('div[2]/text()')[2])
            time.sleep(0.5+random.random())
            m = mPage(self.starturl+list.xpath('div[1]/div/a/@href')[0])
            movie_info = {'title': m.title, 'storage': m.storage, 'url': m.magnet, 'format': list.xpath('div[2]/text()')[2]}
            if self.Update is not None:
                self.Update(movie_info)
            self.item_lists.append(movie_info)
            time.sleep(0.5+random.random())

if __name__ == '__main__':
    x = SearchCiligou(word='战狼')
