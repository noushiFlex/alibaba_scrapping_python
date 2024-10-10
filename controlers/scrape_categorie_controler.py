from models.categorie import Categorie
from models.sous_catgorie import SousCategorie
import csv, os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from models import methode

class CategorieScraper:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    def create_categorie(self):
        try:
            self.categorie_name_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.industry-en-title'))
            )
            self.categorie_name = self.categorie_name_elem.text
            self.cPath = os.getcwd()
            self.categorie = Categorie(nom=self.categorie_name, categorie_path=self.cPath, url=self.url)
            self.categorie.create_folder()
            print(f"Scraping catégorie: {self.categorie.nom}")
            self.sub_categorie_links = self.categorie.get_all_sub_categorie(self.driver)
        except TimeoutException:
            print("Erreur : Le nom de la catégorie n'a pas pu être chargé.")
        except Exception as e:
            print(f"Erreur inattendue lors de la création de la catégorie : {e}")

    def scrape_categorie_products(self):
        with open(self.categorie.pathFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Price', 'Image URL'])

            print(f"Exécution du Scraping : {self.categorie.nom}")

            methode.scroll_to_bottom(self.driver)

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.hugo4-pc-grid-item'))
                )
            except TimeoutException:
                print("Erreur : Les produits n'ont pas pu être chargés à temps.")
                return

            product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.hugo4-pc-grid-item')
            print(f'Produits trouvés: {len(product_elements)}')
            time.sleep(1)

            if not product_elements:
                print("Aucun produit trouvé dans cette catégorie.")
                return

            for number, product in enumerate(product_elements):
                try:
                    products_images = product.find_element(By.CSS_SELECTOR, 'img.picture-image')
                    prodcuts_prices = product.find_element(By.CSS_SELECTOR, 'div.hugo3-util-ellipsis.hugo3-fw-heavy')
                    products_name = product.find_element(By.CSS_SELECTOR, 'div.hugo4-product-element.subject span')

                    img_src = products_images.get_attribute('src')
                    price_text = prodcuts_prices.text
                    product_name = products_name.get_attribute('title')

                    img_name = f"image_article_{number}.png"
                    methode.download_image(img_src, img_name, self.categorie.pathImage)

                    writer.writerow([product_name, price_text, img_src])
                    print(f'Produit: {product_name}, Prix: {price_text}, Image: {img_src}')
                
                except NoSuchElementException:
                    print(f"", end='')

    def scrape_sub_categorie_products(self):
        print("Scraping des sous-categories.")
        for link in self.sub_categorie_links:
            self.sous_categorie = SousCategorie(url=link)
            self.sous_categorie.create_folder(self.categorie.pathCategorie, self.driver)
            print(f"Scraping de la sous categorie : {self.sous_categorie.filter_name}")
            self.sous_categorie.get_all_products()
            
    def main(self):
        try:
            self.driver.get(self.url)
            self.create_categorie()
            self.scrape_categorie_products()
            self.scrape_sub_categorie_products()
            print('Fin du scraping.')
            
        except Exception as e:
            print(f"Erreur inattendue lors de l'exécution principale : {e}")
