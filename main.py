from models.categorie import Categorie
import time, os, csv, requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from views.main_nav import MainNav

firefox_options = Options()
firefox_options.add_argument('--headless')
geckodriver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
s = Service(geckodriver_path)
driver = webdriver.Firefox(service=s, options=firefox_options)

url = "https://www.alibaba.com"

def main():
    nav = MainNav(url, driver)
    nav.show_nav()

if __name__ == "__main__":
    main()
