import pandas as pd
from amazoncaptcha import AmazonCaptcha
# import undetected_chromedriver as web_driver
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json



# url = 'https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/edit#gid=0'

def scraper():
    data_csv = pd.read_csv("amazon_scraping.csv")
    asins = data_csv.loc[:,'Asin']
    countires = data_csv.loc[:,"country"]
    # list of dicts(products)
    products = []
    # each product stored in a dict
    product = {}


    i = 0
    j = 1 # for time

    driver = webdriver.Chrome()
    
    while i < 101:
        if j == 1:
            start_time = time.time()

        asin = str(asins[i])
        country = str(countires[i])
        URL = "https://www.amazon."+country+"/dp/"+asin
        driver.get(URL)
        print(URL)
        error_msg = "URL not found!"
    
        try:
            captcha = AmazonCaptcha.fromdriver(driver)
            solution = captcha.solve()
            product_title = driver.find_element(by=By.CLASS_NAME,value='product-title-word-break').text
            # print(product_title)
            product_img = driver.find_element(by=By.ID, value='landingImage').get_attribute('src')
            # print(product_img)
            product_price = driver.find_element(by=By.CLASS_NAME,value='priceToPay').text
            # print(product_price)
            product_description = driver.find_element(by=By.ID, value='productDescription').text
            # print(product_description)
            product = {'Product Title': product_title,
            'Product Image': product_img,
            'Product Price': str(product_price).replace('\n',"."),
            'Product Description': str(product_description).replace('\n',"")}
            products.append(product)
        except:
            # print('EXCEPT**************')
            product = {'URL': URL,
            'data': error_msg
            }
            products.append(product)

        i += 1
        j += 1
        if j == 100:
            print("Time taken for 100 URLs is:",end=" ")
            print("%s seconds" % (time.time() - start_time))
            j = 1
        
    driver.close()
    with open('products_scraped.json', 'w') as fout:
        json.dump(products, fout, ensure_ascii=False)
    print(products)




if __name__ == "__main__":
    scraper()