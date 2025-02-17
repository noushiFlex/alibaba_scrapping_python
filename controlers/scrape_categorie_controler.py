# Import required models and libraries
from models.categorie import Categorie
from models.sous_catgorie import SousCategorie
import csv, os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from models import methode

class CategorieScraper:
    # Initialize scraper with URL and Selenium driver
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
    
    # Create category and get subcategory links
    def create_categorie(self):
        try:
            # Wait up to 10 seconds for category title element
            self.categorie_name_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.industry-en-title'))
            )
            # Get category name and setup paths
            self.categorie_name = self.categorie_name_elem.text
            self.cPath = os.getcwd()
            # Create category object and folder structure
            self.categorie = Categorie(nom=self.categorie_name, categorie_path=self.cPath, url=self.url)
            self.categorie.create_folder()
            print(f"Scraping category: {self.categorie.nom}")
            # Get all subcategory links
            self.sub_categorie_links = self.categorie.get_all_sub_categorie(self.driver)
        except TimeoutException:
            print("Error: Category name could not be loaded.")
        except Exception as e:
            print(f"Unexpected error while creating category: {e}")
    
    # Scrape products from current category
    def scrape_categorie_products(self):
        # Open CSV file to store product data
        with open(self.categorie.pathFile, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write CSV headers
            writer.writerow(['Product Name', 'Price', 'Image URL'])

            print(f"Starting scraping: {self.categorie.nom}")
            # Scroll to load all products
            methode.scroll_to_bottom(self.driver)

            try:
                # Wait for product grid items to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.hugo4-pc-grid-item'))
                )
            except TimeoutException:
                print("Error: Products could not be loaded in time.")
                return

            # Get all product elements
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.hugo4-pc-grid-item')
            print(f'Products found: {len(product_elements)}')
            time.sleep(1)

            if not product_elements:
                print("No products found in this category.")
                return

            # Extract data from each product
            for number, product in enumerate(product_elements):
                try:
                    # Get product details (image, price, name)
                    products_images = product.find_element(By.CSS_SELECTOR, 'img.picture-image')
                    prodcuts_prices = product.find_element(By.CSS_SELECTOR, 'div.hugo3-util-ellipsis.hugo3-fw-heavy')
                    products_name = product.find_element(By.CSS_SELECTOR, 'div.hugo4-product-element.subject span')

                    # Extract attributes
                    img_src = products_images.get_attribute('src')
                    price_text = prodcuts_prices.text
                    product_name = products_name.get_attribute('title')

                    # Download product image
                    img_name = f"image_article_{number}.png"
                    methode.download_image(img_src, img_name, self.categorie.pathImage)

                    # Write product data to CSV
                    writer.writerow([product_name, price_text, img_src])
                    print(f'Product: {product_name}, Price: {price_text}, Image: {img_src}')
                
                except NoSuchElementException:
                    print(f"", end='')

    # Process all subcategories
    def scrape_sub_categorie_products(self):
        print("Scraping subcategories.")
        for link in self.sub_categorie_links:
            # Create subcategory object and process its products
            self.sous_categorie = SousCategorie(url=link)
            self.sous_categorie.create_folder(self.categorie.pathCategorie, self.driver)
            print(f"Scraping subcategory: {self.sous_categorie.filter_name}")
            self.sous_categorie.get_all_products()
    
    # Main execution method
    def main(self):
        try:
            # Navigate and scrape category and subcategories
            self.driver.get(self.url)
            self.create_categorie()
            self.scrape_categorie_products()
            self.scrape_sub_categorie_products()
            print('Scraping completed.')
            
        except Exception as e:
            print(f"Unexpected error during main execution: {e}")
