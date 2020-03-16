# В файле config.py должны быть строки
# email = 'your_email'
# password = 'your_password'

from config import email, password
from selenium import webdriver
import wget
import os
from glob import glob


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
            download_dict[name + '.mp4'] = mp4
            content_list = self.driver.find_elements_by_class_name('lesson-contents__list-item')
            for content in content_list:
                if 'Методичка ' in content.text:
                    download_dict[content.text + '.pdf'] = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href').split('/')[-2]
                elif 'Презентация' in content.text and '.pptx' in content.text:
                    download_dict[content.text + '.pptx'] = content.find_element_by_class_name('lesson-contents__download-row').get_attribute('href')
        self.driver.quit()
        for name, link in download_dict.items():
            print(f'Качаю {name} {link}')
            if 'Методичка ' in name:
                spam = wget.download(f'https://docs.google.com/document/u/0/export?format=pdf&id={link}')
            else:
                spam = wget.download(link)
            os.rename(spam, folder + '\\' + name)
        print('Завернено')

# wget.download('https://docs.google.com/document/u/0/export?format=pdf&id=1Os4W1-eGgSAgF2CXzImHbTkVuaK-zxELLh7FMR83MC0')


def main():
    folder = input('Введите путь к папке для скачивания ').split('\\')
    folder = '\\\\'.join(folder)
    course_url = input('Введите ссылку на курс ')
    # folder = 'E:\\temp\\'
    # course_url = 'https://geekbrains.ru/chapters/6295'
    driver = webdriver.Chrome()
    parser = Parser(driver, course_url)
    parser.login(email, password)
    parser.download_cource(folder)


if __name__ == '__main__':
    for file in glob('*.tmp'):
        os.remove(file)
    main()
