import math
import re

import selenium
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import numpy as np

chromeOptions = Options()
chromeOptions.add_argument("--start-maximized")
driver = webdriver.Chrome("./chromedriver.exe", chrome_options=chromeOptions)

df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Description"])

search_terms = ['data+scientist', 'machine+learning', 'big+data', 'data+analytics', 'data+science', 'data+mining',
                'statistical+analysis']


def find_cols(soup, job, driver):
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
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
        job_desc = driver.find_element_by_id('vjs-desc').text
    except:
        sum_div.click()
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(5)
        job_desc = driver.find_element_by_id('vjs-desc').text

    return title, location, company, salary, job_desc


def scrap(driver, i, df):
    url = "https://www.indeed.co.uk/jobs?q=" + search + "&l=London%2C+Greater+London&start=" + str(i)
    driver.get(url)
    driver.implicitly_wait(4)

    all_jobs = driver.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html = job.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')

        try:
            title, location, company, salary, job_desc = find_cols(soup, job, driver)
        except selenium.common.exceptions.ElementClickInterceptedException:
            close = driver.find_element_by_xpath('//*[@id="popover-x"]/a')
            close.click()
            title, location, company, salary, job_desc = find_cols(soup, job, driver)

        df = df.append({'Title': title, 'Location': location, 'Company': company,
                        "Description": job_desc}, ignore_index=True)
    return df


for search in search_terms:
    url_start = "https://www.indeed.co.uk/jobs?q=" + search + "&l=London%2C+Greater+London"
    driver.get(url_start)
    driver.implicitly_wait(4)

    pageCount_txt = driver.find_element_by_id('searchCountPages').text
    try:
        pageCount = int(re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1))
    except ValueError:
        pageCount = re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1)
        pageCount = int(pageCount.replace(',', ''))

    for i in np.arange(0, 10000, 10):
        try:
            driver.find_element_by_xpath('//*[@id="resultsCol"]/p/a')
            df = scrap(driver, i, df)
            break
        except selenium.common.exceptions.NoSuchElementException:
            df = scrap(driver, i, df)
        if pageCount <= 10:
            break
df.to_csv("df_broad.csv", index=False)
driver.quit()