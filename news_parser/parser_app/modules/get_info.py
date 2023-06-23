import time

from selenium.webdriver import Keys

from .load_django import *
from parser_app.models import *
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class News:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_links(self, keyword=''):
        # go to website
        print('[+] Opening website')
        self.driver.get('https://tsn.ua/news')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='f-btn f-btn--in f-btn--primary f-btn--upper f-btn--block']")))
        try:
            self.driver.find_element(By.XPATH, "//button[@id='cookieBtn']").click()
        except:
            pass

        # get more news
        # try:
        #     self.driver.find_element(By.XPATH,
        #                              "//button[@class='f-btn f-btn--in f-btn--primary f-btn--upper f-btn--block']").click()
        # except Exception as ex:
        #     print('[ERR]', ex)

        if keyword:
            print('[+] Input keyword')
            self.driver.find_element(By.XPATH, "//button[@id='searchBtn']").click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='searchInput']")))
            key_w = self.driver.find_element(By.XPATH, "//input[@id='searchInput']")
            key_w.clear()
            key_w.send_keys(keyword)
            key_w.send_keys(Keys.ENTER)

        # get links
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='c-card__link']")))
        news_links = self.driver.find_elements(By.XPATH, "//a[@class='c-card__link']")
        print()

        if len(news_links) >= 1:
            j = 1
            for i in range(len(news_links) // 2, len(news_links)):  # get links with text
                print(f'[+] Getting links {j}/{len(news_links) // 2}...')

                news_link = news_links[i].get_attribute('href')
                news_name = news_links[i].text.strip()

                obj, created = Links.objects.get_or_create(
                    link=news_link,
                    name=news_name,
                )

                j += 1
        else:
            print('[ERR] News not found')
        print()

    def get_data(self):
        for l in Links.objects.filter(status='New'):
            url = l.link
            self.driver.get(url)

            print()
            print('########################################################')
            print('URL:', url)

            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='c-bar__img']")))
            except:
                pass

            try:
                name = self.driver.find_element(By.XPATH, "//h1[@class='c-card__title']").text.strip()
            except Exception as ex:
                name = None
            print(name)

            try:
                photo = self.driver.find_element(By.XPATH, "//img[@class='c-card__embed__img']").get_attribute('src')
            except Exception as ex:
                photo = None

            try:
                published = self.driver.find_element(By.XPATH, "//time").text.strip()
            except Exception as ex:
                published = None
            print(published)

            try:
                description_lst = self.driver.find_elements(By.XPATH, "//div[@class='c-article__body']/div[2]/p")
                description = ''
                for txt in description_lst:
                    if txt.text.strip() != 'Читайте також:' and txt.text.strip() != 'Підписуйтесь на наші канали у Telegram та Viber.':
                        description += txt.text.strip()
                        description += '\n'
            except Exception as ex:
                description = None
            print(description)

            defaults = {
                'name': name,
                'photo': photo,
                'published': published,
                'description': description,
            }

            l.status = 'Done'
            l.save()

            obj, created = Articles.objects.get_or_create(
                url=url,
                defaults=defaults,
            )

        self.driver.quit()
