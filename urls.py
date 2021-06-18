"""
Author: Nanasaheb Yadav
Date: 08/06/2021
Description: Scrape URLs of each fund raiser from list of homepage.
get urls for each category and store in list.
"""
try:
    import os
    import time
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError as error:
    print(f"Import Error.... Script Stopped; Error: {error}")


class FundraiserURLS:

    def __init__(self):
        """
        assign variable information to use in other methods.
        """
        self.options = webdriver.ChromeOptions()
        self.options.headless = False
        self.WEBDRIVER_EXE_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe"
        )
        self.driver = webdriver.Chrome(executable_path=self.WEBDRIVER_EXE_PATH, options=self.options)
        self.HOME_URL = 'https://www.impactguru.com/fundraisers'


    def get_fundraiser_urls(self, selector):

        """
        Get URLs of each fundraiser and store it in list.
        input:
        :param selector: Each category selector passed as input to change the category to extract data for each category.
        :return: list of URLs of each fund raiser.
        """

        try:
            # Open Home page here
            self.driver.get(self.HOME_URL)
            time.sleep(5)
            try:
                # change category after opening page
                categories = self.driver.find_element_by_css_selector(selector)
                categories.click()
                time.sleep(5)
                loadingButton = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="loadMoreBtn"]')))
                # load all fund raisers for each category to fetch all fundraisers data
                while True:
                    try:
                        loadingButton.click()
                        time.sleep(2)
                        WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="loadMoreBtn"]')))
                        loadElems = self.driver.find_elements_by_xpath('//*[@id="loadMoreBtn"]')
                        if len(loadElems) > 0:
                            loadingButton = self.driver.find_element_by_xpath('//*[@id="loadMoreBtn"]')
                        else:
                            print("Class: FundraiserURLS; Method: get_fundraiser_urls(); Loaded all the tires")
                            break
                    except:
                        break
            except Exception as err:
                print(f"Class: FundraiserURLS; Method: get_fundraiser_urls(); Error: {err}")
                pass
            time.sleep(5)
            # Get URLS of each fund raiser pages here
            raisers = self.driver.find_elements_by_css_selector('[class="card-body"] a')
            raisers_urls = [url.get_attribute("href") for url in raisers]
            # remove duplicates urls if any
            raisers_urls = list(dict.fromkeys(raisers_urls))
            self.driver.quit()
            return raisers_urls
        except Exception as str_err:
            print(f"Class: FundraiserURLS; Method: get_fundraiser_urls(); Error: {str_err}")
            pass

    def get_urls(self):
        """
        Read All fund raiser urls based on all categories available on portal.
        static coded selector ids mentioned below, as dynamic coded selector ids failed to click on load more buttons.
        after getting all data its stored in csv file for further processing.
        :return: None
        """
        try:
            print(f"Class: FundraiserURLS; Method: get_urls(); Extrating URLs for each Category")
            df = pd.DataFrame()
            sel_dict = {"Medical": '#category-selector > ul > li:nth-child(1)',
                        "NGO": '#category-selector > ul > li:nth-child(2)',
                        "Personal Cause": '#category-selector > ul > li:nth-child(3)',
                        "Creative Ideas": '#category-selector > ul > li:nth-child(4)',
                        "Acid Attacks": '#category-selector > ul > li:nth-child(5)'
                        }
            for key, val in sel_dict.items():
                urls = self.get_fundraiser_urls(val)
                df['urls'] = urls
                df['category'] = key
                df.to_csv('FundRaisers_urls.csv', mode='a', header=False, index=False)
            print(f"Class: FundraiserURLS; Method: get_urls(); Extrating URLs for each Category is Done.")
        except Exception as err:
            print(f"Class: FundraiserURLS; Method: get_urls(); Error: {err}")
            pass


# Remove comment and run it for independently extracting all urls of fundraiser for each category.
# it will save FundRaisers_urls.csv file with appending new data to old data
"""
if __name__ == '__main__':
    obj = FundraiserURLS()
    obj.get_urls()"""