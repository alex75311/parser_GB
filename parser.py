# В файле config.py должны быть строки
# email = 'your_email'
# password = 'your_password'

from config import email, password
from selenium import webdriver
import requests


def remove_chars(value):
    deletechars = '\/:*?"<>|'
    for c in deletechars:
        value = value.replace(c, '')
    return value


class Parser(object):
    def __init__(self, folder):
        self.login_url = 'https://geekbrains.ru/login'
        self.folder = folder
        self.driver = webdriver.Chrome()
        self.download_dict = {}

    def login(self, email, password):  # авторизация
        self.email = email
        self.password = password
        self.driver.get(self.login_url)
        login = self.driver.find_element_by_name('user[email]')
        passwd = self.driver.find_element_by_name('user[password]')
        btn = self.driver.find_element_by_class_name('btn-success')
        login.send_keys(email)
        passwd.send_keys(password)
        btn.click()

    def download_course(self, course_url):  # получаем список уроков
        self.course_url = course_url
        lessons_link = []
        self.driver.get(self.course_url)
        lessons_list = self.driver.find_elements_by_class_name('lesson-header_ended')
        for el in lessons_list:
            if '/tests/' not in el.get_attribute('href'):
                lessons_link.append(el.get_attribute('href'))
        for link in lessons_link:
            self.get_lesson(link)

    def get_lesson(self, link):  # с каждой страницы урока получаем название урока, ссылку на видео и список вложений
        self.driver.get(link)
        mp4 = ''
        while not mp4:
            mp4 = self.driver.find_element_by_tag_name('video').get_attribute('src')
        name = self.driver.find_element_by_tag_name('h3').text
        name = remove_chars(name)
        name += '.mp4'
        self.download_dict[name] = mp4
        content_list = self.driver.find_elements_by_class_name('lesson-contents__list-item')
        for content in content_list:
            try:
                name, link = self.get_correct_link(content)
                self.download_dict[name] = link
            except UnboundLocalError:
                pass
        self.download_files()

    def get_correct_link(self, content):  # получаем имя и ссылку нужных вложений
        if 'Методичка ' in content.text:
            name = content.text + '.pdf'
            link = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href').split(
                'id=')[-1].split('/edit')[0].split('/d/')[-1]
            link = 'https://docs.google.com/document/u/0/export?format=pdf&id=' + link
        elif 'Презентация' in content.text and '.pptx' in content.text:
            name = content.text + '.pptx'
            link = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href')
        return None if not name else name, link

    def download_files(self):  # скачивание и сохранение файла
        for name, link in self.download_dict.items():
            print(f'Качаю {name} {link}')
            r = requests.get(link, stream=True)
            with open(self.folder + name, "wb") as f:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
        print('Завершено')


def main():
    # folder = input('Введите путь к папке для скачивания ').split('\\')
    # folder = '\\\\'.join(folder)
    # course_url = input(
    #     'Введите ссылку на курс (если при нажатии Enter открывается страница в браузере - добавьте в конце пробел ')
    folder = 'E:\\temp\\'
    course_url = 'https://geekbrains.ru/lessons/58831'
    parser = Parser(folder)
    parser.login(email, password)
    # parser.get_lesson(course_url)
    parser.download_course(course_url)


if __name__ == '__main__':
    main()
