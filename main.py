import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from views.main_nav import MainNav

"""
    This is the main file of the project.
    
    It will be used to run the project and to call the different classes and functions 
    that will be used to scrap the data from the website Alibaba.com and to save it in a csv file
    
"""


# Set up the driver
firefox_options = Options()
firefox_options.add_argument('--headless') # Headless mode (hide browser)
geckodriver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
s = Service(geckodriver_path)
driver = webdriver.Firefox(service=s, options=firefox_options)

url = "https://www.alibaba.com" # The url of the website to scrap = Alibaba.com

def main():
    nav = MainNav(url, driver)
    nav.show_nav()

if __name__ == "__main__":
    main()
