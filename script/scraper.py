import math
import re

import selenium
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import numpy as np


def start_webdriver():
    chromeOptions = Options()
    chromeOptions.add_argument("--start-maximized")
    return webdriver.Chrome("script/chromedriver", chrome_options=chromeOptions)


def set_options():
    drv = start_webdriver()
    data_frame = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Description"])
    terms = ['data+scientist', 'machine+learning', 'big+data', 'data+analytics', 'data+science', 'data+mining',
             'statistical+analysis']
    return data_frame, terms, drv


df, search_terms, driver = set_options()


# Title
def scrap_title(soup=None):
    try:
        title = soup.find("a", class_="jobtitle").text.replace('\n', '')
    except:
        title = 'None'
    return title


# Location
def scrap_location(soup=None):
    try:
        location = soup.find(class_="location").text
    except:
        location = 'None'
    return location


# Company
def scrap_company(soup):
    try:
        company = soup.find(class_="company").text.replace("\n", "").strip()
    except:
        company = 'None'
    return company


# Salary
def scrap_salary(soup):
    try:
        salary = soup.find(class_="salaryText").text.replace('\n', '').strip()
    except:
        salary = 'None'
    return salary


# Description
def scrap_description(job):
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
    return job_desc


def find_cols(soup, job):
    title = scrap_title(soup)
    location = scrap_location(soup)
    company = scrap_company(soup)
    salary = scrap_salary(soup)
    job_desc = scrap_description(job)

    return title, location, company, salary, job_desc


def get_page_by_index(drv, index):
    url = "https://www.indeed.co.uk/jobs?q=" + search + "&l=London%2C+Greater+London&start=" + str(index)
    drv.get(url)
    drv.implicitly_wait(4)


def close_popover(drv):
    close = drv.find_element_by_xpath('//*[@id="popover-x"]/a')
    close.click()


def scrap(index, data_frame):
    get_page_by_index(driver, index)

    all_jobs = driver.find_elements_by_class_name('result')

    for job in all_jobs:
        result_html = job.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')

        try:
            title, location, company, salary, job_desc = find_cols(soup, job)
        except selenium.common.exceptions.ElementClickInterceptedException:
            close_popover(driver)
            title, location, company, salary, job_desc = find_cols(soup, job)

        data_frame = data_frame.append({'Title': title, 'Location': location, 'Company': company,
                                        "Description": job_desc}, ignore_index=True)
    return data_frame


def accept_cookies():
    cookies = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
    cookies.click()


def get_homepage():
    url_start = "https://www.indeed.co.uk/jobs?q=" + search + "&l=London%2C+Greater+London"
    driver.get(url_start)
    driver.implicitly_wait(4)
    accept_cookies()


def find_pageCount():
    pageCount_txt = driver.find_element_by_id('searchCountPages').text
    try:
        x = int(re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1))
    except ValueError:
        x = re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1)
        x = int(x.replace(',', ''))
    return x


for search in search_terms:
    get_homepage()
    pageCount = find_pageCount()

    for i in np.arange(0, 10000, 10):
        try:
            driver.find_element_by_xpath('//*[@id="resultsCol"]/p/a')
            df = scrap(i, df)
        except selenium.common.exceptions.NoSuchElementException:
            df = scrap(i, df)
        if pageCount <= 10:
            break
df.to_csv("../data/df_broad.csv", index=False)
driver.quit()
