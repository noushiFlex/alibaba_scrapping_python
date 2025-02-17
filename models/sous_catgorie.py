import os
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.methode import download_image

class SousCategorie:
    
    def __init__(self, url):
        self.url = url
        
    # Create folder for the sous-categorie in the name of sous-categorie and return the paths
    def create_folder(self, categorie_path,driver):
        # Create a folder for the sous-categorie
        self.driver = driver
        self.driver.get(self.url)
        filter_div = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.seb-refine-result_all_filter'))
        )
        self.filter_name = filter_div.find_element(By.CSS_SELECTOR, 'span.seb-refine-result-tag__label').text
        self.safe_sous_categorie_name = ''.join(c for c in self.filter_name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')

        self.sous_categorie_path = os.path.join(categorie_path,self.safe_sous_categorie_name)
        if not os.path.exists(self.sous_categorie_path):
            os.makedirs(self.sous_categorie_path)
        self.image_path = os.path.join(self.sous_categorie_path, 'images')
        self.csv_file_path = os.path.join(self.sous_categorie_path, 'data.csv')

        os.makedirs(self.image_path, exist_ok=True)

        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Product Name', 'Price', 'Image URL'])

        # return self.sous_categorie_path, self.image_path, self.csv_file_path
        
    # Get all products in the sous-categorie
    def get_all_products(self):
        self.driver.get(self.url)
        with open(self.csv_file_path, 'w', newline='') as file: # Open the csv file in write mode
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Price', 'Image URL']) # Write the header of the csv file
            
            # Get all the products in the sous-categorie
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.fy23-search-card.m-gallery-product-item-v2.J-search-card-wrapper.fy23-gallery-card.searchx-offer-item')
            print(f'Produits trouvés: {len(product_elements)}')

            if not product_elements:
                print("Aucun produit trouvé dans cette sous-catégorie.")
                return
            
            # Loop through all the products and get the product name, price and image
            for i, product in enumerate(product_elements):
                img = product.find_element(By.CSS_SELECTOR, 'a.search-card-e-slider__link img')
                price = product.find_element(By.CSS_SELECTOR, 'div.search-card-e-price-main')
                title = product.find_element(By.CSS_SELECTOR, 'h2.search-card-e-title a span')

                img_src = img.get_attribute('src')
                price_text = price.text
                full_text = title.text
                
                img_name = f"image_article_{i}.png"
                download_image(img_src, img_name, self.image_path) # Download the image and save it in the images folder
                
                # Write the product details to the csv file
                writer.writerow([full_text, price_text, img_src])
                print(f'Produit: {full_text}, Prix: {price_text}, Image: {img_src}')
                product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.div.fy23-search-card.m-gallery-product-item-v2.J-search-card-wrapper.fy23-gallery-card.searchx-offer-item')
                if len(product_elements) > i:
                    product = product_elements[i]
