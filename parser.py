# В файле config.py должны быть строки
# email = 'your_email'
# password = 'your_password'

from config import email, password
from selenium import webdriver
import wget
import os


class Parser(object):
    def __init__(self, driver, course_url):
        self.login_url = 'https://geekbrains.ru/login'
        self.course_url = course_url
        self.driver = driver

    def login(self, email, password):
        self.email = email
        self.password = password
        self.driver.get(self.login_url)
        login = self.driver.find_element_by_name('user[email]')
        passwd = self.driver.find_element_by_name('user[password]')
        btn = self.driver.find_element_by_class_name('btn-success')
        login.send_keys(email)
        passwd.send_keys(password)
        btn.click()

    def download_cource(self, folder):
        download_dict = {}
        lessons_link = []
        self.driver.get(self.course_url)
        lessons_list = self.driver.find_elements_by_class_name('lesson-header_ended')
        for el in lessons_list:
            lessons_link.append(el.get_attribute('href'))
        for el in lessons_link:
            self.driver.get(el)
            mp4 = self.driver.find_element_by_tag_name('video').get_attribute('src')
            name = self.driver.find_element_by_tag_name('h3').text
            download_dict[name] = mp4
        for name, link in download_dict.items():
            print(link)
            print(f'Качаю {name}')
            spam = wget.download(link)
            os.rename(spam, folder + name + '.mp4')


def main():
    folder = 'E:\\downloads\\test\\'
    course_url = 'https://geekbrains.ru/chapters/7831'
    driver = webdriver.Chrome()
    parser = Parser(driver, course_url)
    parser.login(email, password)
    parser.download_cource(folder)


if __name__ == '__main__':
    main()
