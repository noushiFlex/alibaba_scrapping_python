# Import required Selenium components and custom controllers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from controlers.scrape_categorie_controler import CategorieScraper

class DefaultScraper:
    # Initialize scraper with base URL and Selenium driver
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    # Fetch all category links from the main page
    def get_categories(self):
        try:
            # Navigate to main URL
            self.driver.get(self.url)
            # Wait for category panel to load (10 seconds timeout)
            panel_content = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.panel-content.secondary-cate-content')))
            # Find all category links in the panel
            category_links = panel_content.find_elements(By.CSS_SELECTOR, 'a')

            # Initialize lists to store category data
            categories = []
            self.categories_link = []
            
            # Extract category information from each link
            for category in category_links:
                try:
                    # Get category name and URL
                    category_name = category.find_element(By.CSS_SELECTOR, 'span.item-name').text
                    category_link = category.get_attribute('href')
                    self.categories_link.append(category_link)
                    categories.append({
                        'name': category_name,
                        'url': category_link
                    })
                except NoSuchElementException:
                    print(f"Error: Unable to retrieve category details")
                    continue

            return categories

        except TimeoutException:
            print("Error: Categories failed to load")
        except Exception as e:
            print(f"Error: {e}")
            
    # Scrape products from selected categories
    def defaultScraping(self):
        # Ask user how many categories to scrape
        for link in self.categories_link[:int(input("Enter number of categories to scrape: "))]:
            # Create category scraper and execute main scraping process
            self.categorieScraping = CategorieScraper(link, self.driver)
            self.categorieScraping.main()

    # Main execution method
    def main(self):
        # Get all categories and start scraping process
        self.get_categories()
        self.defaultScraping()
