from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from controlers.scrape_categorie_controler import CategorieScraper

class DefaultScraper:

    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    def get_categories(self):
        try:
            self.driver.get(self.url)
            panel_content = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.panel-content.secondary-cate-content')))
            category_links = panel_content.find_elements(By.CSS_SELECTOR, 'a')

            categories = []
            self.categories_link = []
            for category in category_links:
                try:
                    category_name = category.find_element(By.CSS_SELECTOR, 'span.item-name').text
                    category_link = category.get_attribute('href')
                    self.categories_link.append(category_link)
                    categories.append({
                        'name': category_name,
                        'url': category_link
                        })

                    # print(f"Catégorie trouvée: {category_name}, URL: {category_link}")
                
                except NoSuchElementException:
                    print(f"Erreur impossible de recuperer les categories")
                    continue

            return categories

        except TimeoutException:
            print("Erreur chargement des categories")
        except Exception as e:
            print(f"Erreur {e}")
            
    def defaultScraping(self):
        for link in self.categories_link[:int(input("Entrez le nombre de categorie a scrapper : "))]:
            self.categorieScraping = CategorieScraper(link,self.driver)
            self.categorieScraping.main()
    def main(self):
        self.get_categories()
        self.defaultScraping()
