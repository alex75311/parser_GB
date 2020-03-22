# В файле config.py должны быть строки
# email = 'your_email'
# password = 'your_password'

from config import email, password
from selenium import webdriver
import wget
import os
from glob import glob
import requests


def remove_chars(value):
    deletechars = '\/:*?"<>|'
    for c in deletechars:
        value = value.replace(c, '')
    return value


class Parser(object):
    def __init__(self, course_url):
        self.login_url = 'https://geekbrains.ru/login'
        self.course_url = course_url
        self.driver = webdriver.Chrome()
        self.folder = ''

    def login(self, email, password):   # авторизация
        self.email = email
        self.password = password
        self.driver.get(self.login_url)
        login = self.driver.find_element_by_name('user[email]')
        passwd = self.driver.find_element_by_name('user[password]')
        btn = self.driver.find_element_by_class_name('btn-success')
        login.send_keys(email)
        passwd.send_keys(password)
        btn.click()

    def get_lessons_link(self):         # получаем список уроков
        lessons_link = []
        self.driver.get(self.course_url)
        lessons_list = self.driver.find_elements_by_class_name('lesson-header_ended')
        for el in lessons_list:
            if '/tests/' not in el.get_attribute('href'):
                lessons_link.append(el.get_attribute('href'))
        return lessons_link

    def get_link(self, link):   # с каждой страницы урока получаем название урока, ссылку на видео и список вложений
        self.driver.get(link)
        mp4 = ''
        while not mp4:
            mp4 = self.driver.find_element_by_tag_name('video').get_attribute('src')
        name = self.driver.find_element_by_tag_name('h3').text
        name = remove_chars(name)
        name += '.mp4'
        content_list = self.driver.find_elements_by_class_name('lesson-contents__list-item')
        return name, mp4, content_list

    def get_correct_link(self, content):        # получаем имя и ссылку нужных вложений
        if 'Методичка ' in content.text:
            name = content.text + '.pdf'
            link = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href').split(
                'id=')[-1].split('/edit')[0].split('/d/')[-1]
            link = 'https://docs.google.com/document/u/0/export?format=pdf&id=' + link
        elif 'Презентация' in content.text and '.pptx' in content.text:
            name = content.text + '.pptx'
            link = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href')
        if not name:
            return None
        return name, link

    def download_files(self, name, link):       # скачивание и сохранение файла
        print(f'Качаю {name} {link}')
        spam = wget.download(link)
        if os.path.exists(self.folder + '\\' + name):
            os.remove(self.folder + '\\' + name)
        os.rename(spam, self.folder + '\\' + name)

    def download_cource(self, folder):          # качаем контент в нужную папку
        self.folder = folder
        download_dict = {}
        lessons_link = self.get_lessons_link()
        for el in lessons_link:
            name, mp4, content_list = self.get_link(el)
            download_dict[name] = mp4

            for content in content_list:
                try:
                    name, link = self.get_correct_link(content)
                    download_dict[name] = link
                except UnboundLocalError:
                    pass

        self.driver.quit()
        print(download_dict)
        for name, link in download_dict.items():
            self.download_files(name, link)
        print('Завернено')


def main():
    # folder = input('Введите путь к папке для скачивания ').split('\\')
    # folder = '\\\\'.join(folder)
    # course_url = input('Введите ссылку на курс ')
    folder = 'E:\\temp\\'
    course_url = 'https://geekbrains.ru/chapters/991'
    parser = Parser(course_url)
    parser.login(email, password)
    parser.download_cource(folder)


if __name__ == '__main__':
    for file in glob('*.tmp'):
        os.remove(file)
    main()
