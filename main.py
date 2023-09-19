import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper import Scraper
from constants import FAIRPRICE_URL, DRIVER_PATH, PROTEIN_SOURCES, ELEMENT_CLASS_NAME
from utils import parse_string_for_query

def main():
    df_product_info = pd.DataFrame()
    with Scraper() as bot:
        for protein_source in PROTEIN_SOURCES:
            # Query for each protein source from site
            bot.land_page(FAIRPRICE_URL + parse_string_for_query(protein_source))
            # Store top 5 products found by the search results
            # Skip first product as it is usually an advertisement
            i = 1
            while i <= 5:
                try:
                    elements = bot.inspect_landing_page_elements()
                    elements[i].click()
                    # Get all product information
                    product_info = bot.get_product_info()
                    # Store in dataframe
                    df_product_info = df_product_info.append(product_info, ignore_index=True)
                    print(df_product_info)
                    bot.return_to_base_url()
                    i += 1
                except:
                    break
    # Save dataframe to csv
    df_product_info.to_csv(r"C:\Users\Admin\Desktop\Projects\Fairprice Scraping and Visualization\product_info.csv")

if __name__ == "__main__":
    main()
