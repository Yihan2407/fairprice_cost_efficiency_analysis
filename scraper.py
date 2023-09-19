import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import *
os.environ['PATH'] += DRIVER_PATH

class Scraper(webdriver.Chrome):
    def __init__(self, driver_path = DRIVER_PATH):
        self.driver_path = driver_path
        self.base_url = ""
        os.environ['PATH'] += self.driver_path
        super(Scraper, self).__init__()

    def land_page(self, url):
        """
        Accesses the product search results.

        Arguments:
        url -- URL of the landing page
        """
        self.alter_base_url(url)
        self.get(url)
        self.implicitly_wait(3)

    def alter_base_url(self, base_url):
        """
        Allows the scraper to store the original search URL and return to it after scraping the product information.

        Arguments:
        base_url -- URL of the base page
        """
        self.base_url = base_url

    def return_to_base_url(self):
        """
        Returns to the base URL.
        """
        self.get(self.base_url)
        self.implicitly_wait(3)

    def inspect_landing_page_elements(self):
        """
        Returns all elements (products) from the landing page
        """
        elements = self.find_elements(By.CLASS_NAME, ELEMENT_CLASS_NAME)
        return elements
    
    def get_product_info(self):
        """
        Returns a dictionary containing the product's information
        """
        # Get price
        price = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            PRICE_XPATH))).text

        # Get product name
        product_name = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            PRODUCT_NAME_XPATH1))).text
        if product_name.split(" ")[0] == "Till" or product_name.split(" ")[0] == "Ends": # Has sales tag, use XPATH2
            product_name = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                PRODUCT_NAME_XPATH2))).text

        # Get product weight -- Try two different XPATHs
        try:
            product_weight = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                PRODUCT_WEIGHT_XPATH1))).text
        except:
            try:
                product_weight = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    PRODUCT_WEIGHT_XPATH2))).text   
            except:
                product_weight = 0

        # Get nutritional information
        try:
            nutritional_elements = self.find_elements(By.CLASS_NAME, NUTRITIONAL_INFO_CLASS_NAME)
        except NoSuchElementException:
            nutritional_elements = {}
        nutrition_info = {}
        # Parse nutritional information
        if nutritional_elements:
            for element in nutritional_elements:
                innerText = element.get_attribute("innerText")
                nutrition_info[innerText.split("\n")[0]] = innerText.split("\n")[1]

        # Compile product information
        product_info = {
            "product_name": product_name,
            "price": price,
            "product_weight": product_weight,
            "nutritional_elements": nutrition_info
        }
        
        # Convert nutritional information to JSON
        product_info['nutritional_elements'] = json.dumps(product_info['nutritional_elements'])
        return product_info        

    