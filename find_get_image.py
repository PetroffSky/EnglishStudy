from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import json
import wget
import os, os.path


class Find_Get:
    def __init__(self):
        with open('words.txt', 'r', encoding='utf-8') as words:
            self.word_list = list(filter(lambda a: len(a) > 0, words.read().split('\n')))
            print(f"Готовим изображения для следующих слов: {self.word_list}")

        self.link = 'https://yandex.ru/images/search'
        self.get_browser()


    # Создаём объект браузера с настройками
    def get_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # запуск в режиме инкогнито
        options.add_argument("start-maximized")  # запуск в развёрнутым экраном
        options.add_argument("user-agent=Mozilla/5.0 "
                             "(Windows NT 6.3; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36")

        # отключаем надпись об автоматизированном программном обеспечении
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Открываем браузер и настраиваем его
        with webdriver.Chrome(options=options) as self.browser:
            self.browser.implicitly_wait(5)
            self.browser.get(self.link)
            pic_size = self.browser.find_elements('xpath', "//button[contains(@class, 'Button2_size_m')]")[0]
            pic_size.click()
            input_size_w = self.browser.find_element('xpath', "//input[@placeholder='1366']")
            input_size_w.click()
            input_size_w.send_keys('500')
            input_size_h = self.browser.find_element('xpath', "//input[@placeholder='768']")
            input_size_h.click()
            input_size_h.send_keys('500')
            input_size_h.send_keys(Keys.ENTER)
            self.image_finder()


    # Ищем изображение по слову из списка
    def image_finder(self):
        for word in self.word_list:
            self.word = word
            input_field = self.browser.find_element('xpath', "//input[@name='text']")
            input_field.click()
            input_field.send_keys(f"{self.word}")
            input_field.send_keys(Keys.ENTER)
            # Нажимаем на первую картинку в поисковых результатах
            time.sleep(3)
            img_clck = self.browser.find_element('xpath', "//div[@class='serp-item__meta']")
            img_clck.click()
            # Открываем картинку в другой вкладке
            open_image = self.browser.find_element('xpath', "//span[contains(text(), 'Открыть')]/..")
            open_image.click()
            # Переключаемся на открытую вкладку и получаем URL файла
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.url = self.browser.current_url
            print(self.url)
            # Закрываем открытую вкладку и переключаемся на 1-е окно
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.back()
            # Очищаем поле ввода
            input_field.clear()
            time.sleep(1)
            self.image_downloader()


    # Скачиваем изображение и сохраняем его в файл
    def image_downloader(self):
        self.path = f'Results/Images/{self.word}.jpg'
        if os.path.isfile(self.path): os.remove(self.path)
        try:
            filename = wget.download(self.url)
            os.rename(filename, self.path)
            print(f"Downloading file {self.word} is Done")
        except Exception as ex:
            print(f'Downloading is Fail! Cause: {ex}')


