import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import os
import login
from urllib.request import urlopen

import requests
import csv
import datetime

class LinkedinJobScrape:

    #initializing drivers
    def __init__(self,username,password,location):

        self.language = language
        self.options = self.browser_options()
        options.headless=False
        prefs={"profile.default_content_setting_values.notofications" :2}
        options.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        #self.start_linkedin(username,password)

    #authenticating username and password
    def authenticate_linkedin(self,username,password):
        # driver.get method() will navigate to a page given by the URL address
        driver.get('https://www.linkedin.com')
        # locate email form by_class_name
        username = driver.find_element_by_class_name('login-email')
        # send_keys() to simulate key strokes
        username.send_keys(parameters.linkedin_username)
        # sleep for 0.5 seconds
        sleep(0.5)
        # locate password form by_class_name
        password = driver.find_element_by_class_name('login-password')
        # send_keys() to simulate key strokes
        password.send_keys(parameters.linkedin_password)
        sleep(0.5)
        # locate submit button by_xpath
        sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
        # .click() to mimic button click
        sign_in_button.click()

    def start_apply(self,username,password):
        self.authenticate_linkedin(username,password)
        self.fill_data()
        self.extract_details()

    def exract_details(self):
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)
        urls = []
   
        urls=self.get_links(self.browser.get(url)
        #looping through every url and getting details
        for url in urls :
            data = {}
            self.browser.find_element_by_xpath(
                '//button[@aria-controls="job-details"]'
                ).click()
            self.browser.find_element_by_class_name(
                'view-more-icon'
                ).click()
            self.load_page(sleep=1)

            data['jobTitle'] = self.browser.find_element_by_xpath(
                    '//h1[@class="jobs-top-card__job-title t-24"]'
                    ).text.strip()
 
            data['company'] = self.browser.find_element_by_xpath(
                    '//span[contains(text(),"Company Name")]/following::a'
                    ).text.strip()    
            
            data['jobLocation'] = self.browser.find_element_by_xpath(
                    '//span[contains(text(),"Company Location")]/following::span'
                    ).text.strip()
            

            data['no. applicants']  = self.browser.find_element_by_xpath(
                    '//span[contains(text(),"Number of applicants")]/following::span'
                    ).text.strip()
                    
            data['job description'] = self.browser.find_element_by_xpath(
                    '//div[@id="job-details"]'
                    ).text.strip().replace('\n', ', ')
            

            data['jobIndustries'] = self.browser.find_element_by_xpath(
                    '//h3[contains(text(),"Industry")]/following::*'
                    ).text.strip()

            with open('linkedin_details.csv', 'w', newline='') as f:
                writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])
                writer = csv.writer(f)
                writer.writerow(data.values())
                
    def get_job_links(self, html_page):
        links = []
        for link in html_page.find_all('a'):
            url = link.get('href')
            if '/jobs/view' in url:
                links.append(url)
        return set(links)

    def get_job_page(self, job):
        root = 'www.linkedin.com'
        if root not in job:
            job = 'https://www.linkedin.com'+job
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

    #fetching the next job page
    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            "https://www.linkedin.com/jobs/search/?keywords=" +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.load_page()
        scroller = 0
        self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
        time.sleep(2000)
        pages = BeautifulSoup(self.browser.page_source, "lxml")
        return (self.browser, pages)


if __name__ == '__main__':
        
    #enter the username and password before running the script
    username = ''
    password = ''
    location = 'Canada'
    
    #start the scraping process
    scrape = LinkedinJobScrape(username,password position, location)
    scrape.start_apply(username,password,location)