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
