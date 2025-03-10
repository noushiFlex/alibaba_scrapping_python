from controlers.scrape_default_controler import DefaultScraper
from controlers.scrape_categorie_controler import CategorieScraper
from pyfiglet import Figlet
import os

# Main navigation class
class MainNav:
    
    def __init__(self, url_principale, driver):
        self.url = url_principale
        self.driver = driver
     
    # Show the main navigation
    def show_nav(self):
        while True:
            
            f = Figlet(font='doom')
            os.system('cls')
            
            print(f.renderText('Web Scrapper'))
            print(f'\t1 - Scraper une catégorie \n\t2 - Scrapping par défaut \n\t0 - Quitter \n')
            choix = input("Votre choix : ")
            
            # Check if the choice is valid
            if not choix.isnumeric() or int(choix) not in [0, 1, 2]:
                print("Entrez un choix valide.")
                continue
            choix = int(choix)
            # Close the driver and exit the program
            if choix == 0:
                break
            # Scrap one category
            elif choix == 1:
                url = input("Veuillez entrer l'url : ")
                categorieScrap = CategorieScraper(url=url,driver=self.driver)
                categorieScrap.main()
                break
            # Scrap the 10 defautls categories
            elif choix == 2:
                DefaultScrap = DefaultScraper(self.url,self.driver)
                DefaultScrap.main()
                break