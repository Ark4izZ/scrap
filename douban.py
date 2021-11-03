from time import sleep

import requests
from lxml import etree


class DouBan(object):
    def __init__(self):
        self.url = "https://movie.douban.com/top250"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
                    'Cookie':''}
        self.proxies = {
            "http": "http://113.204.239.91:8081"
        }

    def get_data(self, url):
        res = requests.get(url=url, headers=self.headers, proxies=self.proxies).content.decode("utf-8")
        return res

    def parse_data(self, res):
        html = etree.HTML(res)

        # 提取链接
        link_list = html.xpath("//*/li/div/div/a/@href")  # 电影链接

        # 电影名提取
        movie_list = html.xpath("//span[@class='title'][1]/text()")

        data_list =[]
        for link, movie in zip(link_list,movie_list):
            data_list.append(link + movie+"\n")

        # 获取下一页链接
        try:
            url_next = self.url + html.xpath(r'//*[@id="content"]//span[@class="next"]/link/@href')[0]  # 下一页链接
        except:
            url_next = None

        self.save_data(data_list)

        return url_next

    def save_data(self, data_list):
        # 写入txt
        with open("豆瓣250.txt", "ab") as f:
            for data in data_list:
                f.write(data.encode("utf-8"))

    def run(self):
        url_next = self.url
        while True:

            res = self.get_data(url_next)
            url_next = self.parse_data(res)
            if url_next==None:
                break


if __name__ == '__main__':
    douban = DouBan()
    douban.run()



