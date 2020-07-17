from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

driver = webdriver.Chrome("./chromedriver.exe")
driver.set_window_size(1920, 1080)

df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Description"])

'''
search_terms = ['data+scientist', 'machine+learning', 'big+data', 'data+analytics', 'data science', 'data+mining',
                'statistical+analysis']
'''

search_terms = ['data+science']

for search in search_terms:
    for i in range(0, 50, 10):
        i_check = i
        url = "https://www.indeed.co.uk/jobs?q=" + search + "&l=London%2C+Greater+London&start=" + str(i)
        driver.get(url)
        driver.implicitly_wait(4)

        all_jobs = driver.find_elements_by_class_name('result')

        for job in all_jobs:

            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            # Title
            try:
                title = soup.find("a", class_="jobtitle").text.replace('\n', '')
            except:
                title = 'None'
            # location
            try:
                location = soup.find(class_="location").text
            except:
                location = 'None'
            # company
            try:
                company = soup.find(class_="company").text.replace("\n", "").strip()
            except:
                company = 'None'
            # salary
            try:
                salary = soup.find(class_="salaryText").text.replace('\n', '').strip()
            except:
                salary = 'None'
            # Description
            sum_div = job.find_elements_by_class_name("summary")[0]
            try:
                sum_div.click()
            except:
                close_button = driver.find_elements_by_class_name('popover-x-button-close')
                try:
                    close_button[0].click()
                except:
                    close_button.click()
                sum_div.click()

            job_desc = driver.find_element_by_id('vjs-desc').text

            df = df.append({'Title': title, 'Location': location, 'Company': company,
                            "Description": job_desc}, ignore_index=True)

df.to_csv("df_broad.csv", index=False)
