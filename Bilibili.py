import json
import time
from selenium import webdriver

# save部分还没有做好


class Bilibili(object):
    def __init__(self):
        self.url = "https://www.bilibili.com/v/popular/all"
        self.driver = webdriver.Chrome('../driver/chromedriver')

    def parse_data(self):
        time.sleep(2)
        # h = int(self.driver.execute_script('document.documentElement.scrollHeight'))
        x = 0
        while x < 20000:
            # document.documentElement.scrollHeight
            js = 'window.scrollTo({},{})'.format(x, x+100)
            self.driver.execute_script(js)
            x += 100
            time.sleep(0.1)

        videos = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/ul/div')
        # print("waiting")
        print(len(videos))
        data = []
        for video in videos:
            temp = {'title': video.find_element_by_xpath('.//p').text,
                    'up': video.find_element_by_xpath('.//span[@class="up-name__text"]').text,
                    'click': video.find_element_by_xpath(".//p[@class='video-stat']/span[@class='play-text']").text,
                    'pic': video.find_element_by_xpath('./div/a/img').get_attribute('src'),
                    'link': video.find_element_by_xpath('./div/a').get_attribute('href')}
            # print(temp)
            data.append(temp)
        self.driver.quit()

        # print(len(data))

        return data

    def save(self, datas):
        for data in datas:
            with open('b站热门.txt', 'wb') as f:
                f.write((json.dumps(data)+'\n').encode("utf-8"))

    def run(self):
        self.driver.get(self.url)
        data = self.parse_data()
        self.save(data)


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.run()