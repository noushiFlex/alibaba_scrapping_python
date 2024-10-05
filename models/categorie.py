import os
import csv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Categorie:
    def __init__(self, nom, url, categorie_path):
        self.nom = nom
        self.url = url
        self.safe_categorie_name = ''.join(c for c in self.nom if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
        self.categorie_path = categorie_path

    def create_folder(self):
        self.pathCategorie = os.path.join(self.categorie_path, 'data', self.safe_categorie_name)
        if not os.path.exists(self.pathCategorie):
            os.makedirs(self.pathCategorie)

        self.pathImage = os.path.join(self.pathCategorie, 'images')
        if not os.path.exists(self.pathImage):
            os.makedirs(self.pathImage)

        self.pathFile = os.path.join(self.pathCategorie, 'data.csv')
        if not os.path.exists(self.pathFile):
            with open(self.pathFile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Product Name', 'Price', 'Image URL'])

    def get_all_sub_categorie(self, driver):
        self.product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.hugo4-pc-grid-item')
        if not self.product_elements:
            print("Aucun produit trouvé dans cette catégorie.")
            return []

        links = []
        while True:
            try:
                n = int(input(f"Entrez le nombre de sous-catégories à scrapper (max {len(self.product_elements)}) : "))
                if n <= len(self.product_elements):
                    for i, product in enumerate(self.product_elements[:n]):
                        try:
                            link_element = product.find_element(By.CSS_SELECTOR, 'a.hugo-dotelement')
                            product_link = link_element.get_attribute('href')
                            links.append(product_link)
                        except NoSuchElementException:
                            print(f"Erreur : Aucun lien trouvé pour le produit {i + 1}.")
                    break 
                else:
                    print(f"Il n'y a que {len(self.product_elements)} sous-catégories disponibles.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide.")

        return links
