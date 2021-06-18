"""
Author: Nanasaheb Yadav
Date: 08/06/2021
Description: Scrap each fund raiser page and store it in csv file
"""

try:
    import os
    import time
    import pandas as pd
    from selenium import webdriver
    from urls import FundraiserURLS
except Exception as error:
    print(f"Import Error... Exiting.. {error}")


class Scrapper:

    def __init__(self):

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.WEBDRIVER_EXE_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe"
        )

        self.fund_raiser_obj = FundraiserURLS()

    def scrap_fundraisers(self):
        """
        Scrap each url present in FundRaisers_urls.csv file and store all result in one file.
        :return:
        """
        output_list = []
        title, campaigner, beneficiary, banner, story, bank_account, raised_amount, top_influencer, actual_raised = "", "", "", "", "", "", "", "", ""
        try:
            csv_reader = pd.read_csv(os.path.abspath('FundRaisers_urls.csv'))
            urls = csv_reader.values.tolist()
            driver = webdriver.Chrome(executable_path=self.WEBDRIVER_EXE_PATH, options=self.options)
            driver.maximize_window()
            for ic, (url, category) in enumerate(urls):
                try:
                    print("start", ic + 1)
                    title, campaigner, beneficiary, banner, story, bank_account, raised_amount, top_influencer, actual_raised = "", "", "", "", "", "", "", "", ""
                    url = url.strip()
                    driver.get(url)

                    title_node = driver.find_element_by_css_selector('#campaignTitle')
                    if not title_node:
                        title_node = driver.find_element_by_css_selector('body > div:nth-child(3) > div > section.mt-3 > div > div:nth-child(2) > div')

                    campaigner_node = driver.find_element_by_css_selector('body > div:nth-child(3) > div > section.hiw-4.mb-3.mb-md-4-5 > div > div > div.col-lg-7.px-0.px-sm-3.my-sm-4.my-lg-0 > div.d-none.d-sm-flex.flex-wrap.w-100.px-2 > div.flex-1.mr-3 > div > div.details-card__content.flex-1')
                    if not campaigner_node:
                        campaigner_node = driver.find_element_by_css_selector('body > div:nth-child(3) > div > section.hiw-4.mb-3.mb-md-4-5 > div > div > div.col-lg-7.px-0.px-sm-3.my-sm-4.my-lg-0 > div.d-none.d-sm-flex.flex-wrap.w-100.px-2 > div.flex-1.mr-3 > div > div.details-card__content.flex-1 > div.title')

                    beneficiary_node = driver.find_element_by_css_selector('body > div:nth-child(3) > div > section.hiw-4.mb-3.mb-md-4-5 > div > div > div.col-lg-7.px-0.px-sm-3.my-sm-4.my-lg-0 > div.d-none.d-sm-flex.flex-wrap.w-100.px-2 > div:nth-child(2) > div > div.details-card__content.flex-1')
                    if not beneficiary_node:
                        beneficiary_node = driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div/div[1]/div[2]/div[2]/div/div[2]')

                    banner_node = driver.find_element_by_css_selector('#campaignCarousel > div.carousel-inner.card-shadow > div > picture > img')
                    if not banner_node:
                        banner_node = driver.find_element_by_xpath('//*[@id="campaignCarousel"]/div[1]/div/picture')

                    story_node = driver.find_element_by_css_selector('#story-block > div')
                    if not story_node:
                        story_node = driver.find_element_by_xpath('//*[@id="story-block"]/div')

                    account_node = driver.find_element_by_css_selector('#payment-options > div > div.p-3.h-100.d-inline-block.w-100.align-top')
                    if not account_node:
                        account_node = driver.find_element_by_xpath('//*[@id="payment-options"]/div/div[2]')

                    amount_node = driver.find_element_by_css_selector('#left-side-fr > div > div:nth-child(1) > div:nth-child(1) > div.p-1.mt-1.mb-3.d-none.d-sm-block.box-stick__border-light > div.h-100.d-inline-block.w-100.align-top.mt-0.side-t-con.text-center > h4')
                    if not amount_node:
                        amount_node = driver.find_element_by_xpath('//*[@id="left-side-fr"]/div/div[1]/div[1]/div[1]/div[2]/h4')

                    top_influencer_node = driver.find_element_by_xpath('//*[@id="promoters"]/div/div/div[2]/div[2]')
                    if not top_influencer_node:
                        top_influencer_node = driver.find_element_by_css_selector('#promoters > div > div > div.details-card__content > div.description.grey-text')

                    actual_amount = driver.find_element_by_css_selector('#left-side-fr > div > div:nth-child(1) > div:nth-child(1) > div.p-1.mt-1.mb-3.d-none.d-sm-block.box-stick__border-light > div.h-100.d-inline-block.w-100.align-top.mt-0.side-t-con.text-center > h4 > span.custom-raisedAmount')
                    if not actual_amount:
                        actual_amount = driver.find_element_by_xpath('//*[@id="left-side-fr"]/div/div[1]/div[1]/div[1]/div[2]/h4/span[1]')


                    if title_node:
                        title = title_node.text
                    if campaigner_node:
                        campaigner = campaigner_node.text
                    if beneficiary_node:
                        beneficiary = beneficiary_node.text
                    if banner_node:
                        banner= banner_node.get_attribute('src')
                    if story_node:
                        story = story_node.text
                    if account_node:
                        bank_account = account_node.text
                    if amount_node:
                        raised_amount = amount_node.text
                    if top_influencer_node:
                        top_influencer = top_influencer_node.text
                    if actual_amount:
                        actual_raised = actual_amount.text
                    output_list.append([category, url, title, campaigner, beneficiary, banner, story, bank_account, raised_amount, top_influencer, actual_raised])
                except:
                    output_list.append([category, url, title, campaigner, beneficiary, banner, story, bank_account, raised_amount, top_influencer, actual_raised])

            driver.quit()
        except Exception as error:
            print(f"Class: Scrapper; Method: main(); Error: {error}")
            pass
        new_output = [["category", "url", "title", "campaigner", "beneficiary", "banner", "story", "bank_account", "raised_amount", "top_influencer", "actual_raised"]] + output_list[:]

        my_df = pd.DataFrame(new_output)
        my_df.to_csv('ImpactGuru.csv', index=False, header=False)
        return 'ImpactGuru.csv'


    def plot_data(self, filename):
        """
        Create table based on category field and store it in html file.
        Please open Summary_Chart.html file after running the code for output
        :return:
        """
        try:
            if not filename:
                df = pd.read_csv('ImpactGuru.csv')
            else:
                df = pd.read_csv(filename)
            df.fillna(0)
            df.dropna()
            df = df.groupby('category').count()
            code = df.to_html(na_rep=0)
            html_file = open("Summary_Chart.html", "w")
            html_file.write(code)
            html_file.close()
            return os.path.abspath('Summary_Chart.html')
        except Exception as error:
            print(f"Class: Scrapper; Method: plot_data(); Error: {error}")


    def main(self):
        """
        Here all modules called one by one for complete automation.
        it returns html page url which contains summary chart. Please open file for reference.
        :return:
        """
        print("******************BIGIN***********************")
        self.fund_raiser_obj.get_urls()
        filename= self.scrap_fundraisers()
        chart= self.plot_data(filename)
        print(f"Use {chart} html file to get summarized report. for scrapped data please open {filename} present in project folder")
        print("*******************END********************\n THANK YOU!!")

if __name__ == '__main__':
    obj = Scrapper()
    obj.main()