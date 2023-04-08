#!/usr/bin/env python
# coding: utf-8

# # ************************** LinkedIn Job Scraping ************************ #

# ##### Aishwarya Prashant Kamat
# ##### Qian(Lucy) Wu
# ##### Haridhakshini (Harisha) Subramoniapillai Ajeetha

# # Readme
# 
# Since we using ipywidgets and IPython.display  packages specifically designed for Jupyter Notebook and other Jupyter environments, we request you to use the Jupyter Notebook for executing the code and not the .py file. The Source code has four user-defined functions in the main function. They are 
# 
# 1. ScrapingToMongoDb()
# 2. Generate_Form()
# 3. Filtering()
# 4. Future_Salary_Filter()
# 
# Please run only the functions you are interested in. 
# The first function ScrapingToMongoDb()  when run will prompt you to enter a job title you are interested in.
# The filtering () function will prompt you to input values into the form. 
# 
# The MongoDB database data dump is present in the compressed folder as BSON dump. 
# 
# There is an ADDITIONAL FILTERING section towards the end of the notebook to illustrate the functions of the filtering
# application.
# 
# 
# ###### Please run the 4 functions and scroll down to the main function to begin execution. 

# ### Loading the required Modules

# In[1]:


from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import re
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
user_agent = {'User-agent': 'Mozilla/5.0'} 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
import pyautogui # to press down arrow key
from html.parser import HTMLParser 
import datetime
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import ipywidgets as widgets
from IPython.display import display


# ### Enter the Job you are interested in

# In[14]:


def ScrapingToMongoDb():
    user_input = input("Enter the Job you are interested in: ")

    # Print the input string
    print("You entered:", user_input)

    # Using Selenium to search and Scroll through LinkedIn jobs

    browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver.exe")
    browser.maximize_window()
    url= "https://www.linkedin.com/"

    browser.get(url)
    time.sleep(2)

    ###################################################################################################
    # Open LinkedIn website and click on Jobs
    ###################################################################################################

    url = "https://www.linkedin.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)

    jobs_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/nav/ul/li[4]/a'))
    )
    jobs_link.click()

    search_bar = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search job titles or companies']"))
    )
    search_bar.click()

    search_bar.send_keys(user_input) 
    search_bar.send_keys(Keys.RETURN)

    time.sleep(5)

    ###################################################################################################
    # Keep scrolling and load more jobs(5 times)
    ###################################################################################################
    for i in range(2): # You can change this to scrape for more jobs
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)
        pyautogui.press('down',presses=100)


        ShowMoreJobs_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/section[2]/button'))).click()

    ###################################################################################################
    #Write page source to HTML file and download it. 
    ###################################################################################################

    pageSource = browser.page_source

    fileToWrite = open("LinkedIn_Source.html", "w")
    fileToWrite.write(pageSource)

    print("Downloaded LinkedIn_Source.html file Successfully!")
    fileToWrite.close()

    #Create Beautiful soup object
    fileToRead = open("LinkedIn_Source.html", "r")
    soup = BeautifulSoup(fileToRead.read())

    JobLinks = []
    card_list = soup.find_all('div', {'class': 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'})
    for card in card_list:
        link = card.find('a')['href']
        JobLinks.append(link)

    print(len(JobLinks))

    # Download the HTML files

    i=1 # Last index of the HTML file downloaded
    for link in JobLinks:
        response = requests.get(link,headers = user_agent)
        soup1 = BeautifulSoup(response.content, 'html.parser')

        with open("Linkedin_Job_NEW_[%d].html"%(i), "w", encoding='utf-8') as file:
            file.write(soup1.prettify())
            file.close()
        i=i+1

    # Parsing the content

    ###################################################################################################
    # Defining Empty Lists
    Job_Title=[]
    CName = []
    CUrl = []
    Job_Location = []
    No_of_Applicants = []

    Recruiter_Name = []
    Recruiter_Title = []
    Recruiter_Url = []

    Job_Descriptions=[]
    Job_Levels=[]
    Job_Types=[]
    Job_function =[]
    Job_Industry =[]
    Similar_Jobs_Links=[]
    Date_Downloaded=[]
    Date_Posted=[]
    ###################################################################################################

    for i in range(len(JobLinks)):
    #for i in range(940,1038):
        with open("Linkedin_Job_NEW_[%d].html"%(i+1), 'r') as file: # Change the file name
            html = file.read()
            soup_html = BeautifulSoup(html, 'html.parser')

            #TITLE
            if (soup_html.select('#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div>h1')):
                title = soup_html.select('#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div>h1')
                Job_Title.append(title[0].text.strip())
            else:
                Job_Title.append(None)

            #Company name and #Company LinkedIn URL

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span:nth-child(1) > a")):
                name = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span:nth-child(1) > a")
                CName.append(name[0].text.strip())
                CUrl.append(name[0].get("href"))
            else:
                CName.append(None)
                CUrl.append(None)


            # Job location

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span.topcard__flavor.topcard__flavor--bullet")):        
                loc = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span.topcard__flavor.topcard__flavor--bullet")
                Job_Location.append(loc[0].text.strip())
            else:
                 Job_Location.append(None)

            # Number of Applicants

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > figure > figcaption")):
                num = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > figure > figcaption")
                No_of_Applicants.append(num[0].text.strip())
            else:
                No_of_Applicants.append(None)

            #RECRUITER DETAILS

            # Rec Name
            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > img")):

                rec_name = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > img")
                Recruiter_Name.append(rec_name[0]['alt'])
            else:
                Recruiter_Name.append(None)


            # Rec Title

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > div.base-main-card__info.self-center.ml-1.flex-1.relative.break-words.papabear\:min-w-0.mamabear\:min-w-0.babybear\:w-full > h4")):
                rec_title = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > div.base-main-card__info.self-center.ml-1.flex-1.relative.break-words.papabear\:min-w-0.mamabear\:min-w-0.babybear\:w-full > h4")
                Recruiter_Title.append(rec_title[0].text.strip())
            else:
                Recruiter_Title.append(None)

            #Rec Link
            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > div.base-main-card__ctas.z-\[3\].self-center.ml-3.babybear\:ml-1.babybear\:self-start > a")):
                rec_message_link = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.message-the-recruiter > div > div.base-main-card__ctas.z-\[3\].self-center.ml-3.babybear\:ml-1.babybear\:self-start > a")
                Recruiter_Url.append(rec_message_link[0].get("href"))
            else:
                Recruiter_Url.append(None)

            # JOB DESCRIPTION

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.description__text.description__text--rich > section > div")):

                job_descr = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > div.description__text.description__text--rich > section > div")
                Job_Descriptions.append(job_descr[0].text.strip())
            else:
                Job_Descriptions.append(None)

            # JOB LEVEL

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(1) > span")):
                job_level = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(1) > span")
                Job_Levels.append(job_level[0].text.strip())

            else:
                Job_Levels.append(None)

            # JOB TYPE

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(2) > span")):
                type_job = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(2) > span")
                Job_Types.append(type_job[0].text.strip())

            else:
                Job_Types.append(None)

            # JOB FUNCTION

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(3) > span")):
                function_job = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(3) > span")
                Job_function.append(function_job[0].text.strip())
            else:
                Job_function.append(None)

            # JOB INDUSTRY

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(4) > span")):
                industry_job = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > div > section.core-section-container.my-3.description > div > ul > li:nth-child(4) > span")
                Job_Industry.append(industry_job[0].text.strip())
            else:
                Job_Industry.append(None)

            # SIMILAR JOB LINKS

            if (soup_html.find_all('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})):
                similar_jobs_cards = soup_html.find_all('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})

                Similar_Jobs_Links_for_this_job =[]
                for card in similar_jobs_cards:
                    sim_link = card.get('href')
                    Similar_Jobs_Links_for_this_job.append(sim_link)

                Similar_Jobs_Links.append(Similar_Jobs_Links_for_this_job)
            else:
                Similar_Jobs_Links.append(None)

            # DATE DOWNLOADED
            today = str(datetime.date.today())
            Date_Downloaded.append(today)

            # DATE POSTED

            if (soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > span")):
                posted = soup_html.select("#main-content > section.core-rail.mx-auto.papabear\:w-core-rail-width.mamabear\:max-w-\[790px\].babybear\:max-w-\[790px\] > div > section.top-card-layout.container-lined.overflow-hidden.babybear\:rounded-\[0px\] > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > span")
                Date_Posted.append(posted[0].text.strip())
            else:
                Date_Posted.append(None)

    # ################################################################################################################

    print("JOB TITLES")
    print(Job_Title)
    print("\n")

    print("COMPANY NAMES")
    print(CName)
    print("\n")

    print("COMPANY URLS")
    print(CUrl)
    print("\n")

    print("JOB LOCATIONS")
    print(Job_Location)
    print("\n")

    print("# APPLICANTS")
    print(No_of_Applicants)
    print("\n")

    print("#DATE POSTED")
    print(Date_Posted)
    print("\n")

    print("DATE DOWNLOADED")
    print(Date_Downloaded)
    print("\n")

    # ################################################################################################################

    print("RECRUITER NAME")
    print(Recruiter_Name)
    print("\n")

    print("RECRUITER TITLE")
    print(Recruiter_Title)
    print("\n")

    print("RECRUITER LINKEDIN URL")
    print(Recruiter_Url)
    print("\n")

    # ################################################################################################################

    print("JOB DESCRIPTIONS")
    print(Job_Descriptions)
    print("\n")

    print("JOB LEVELS")
    print(Job_Levels)
    print("\n")

    print("JOB TYPES")
    print(Job_Types)
    print("\n")

    print("JOB FUNCTIONS")
    print(Job_function)
    print("\n")

    print("JOB INDUSTRY")
    print(Job_Industry)
    print("\n")

    print("SIMILAR JOBS")
    print(Similar_Jobs_Links) 
    print("\n")   

    # ################################################################################################################

    # Connecting to Mongo DB

    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client["LinkedIn_DB"]

    collection1 = db["JOBS_Basic"]
    collection2 = db["JOBS_Recruiter"]
    collection3 = db["JOBS_DESCRIPTION"]
    collection4 = db["JOBS_Advanced"]

    # Inserting into the MongoDB

    import datetime

    x=0
    for i in range(len(JobLinks)-1):

        data1 = {
                    "ID": x+1,
                    "TITLE": Job_Title[i],
                    "COMPANY": CName[i],
                    "LOCATION": Job_Location[i],
                    "#Applicants": No_of_Applicants[i],
                    "Date Posted": Date_Posted[i],
                    "Job URL": JobLinks[i],
                    "Company URL": CUrl[i],
                    "Date_Downloaded" : Date_Downloaded[i]                
                }

        data2 = {
                    "ID": x+1,
                    "Recruiter Name": Recruiter_Name[i],
                    "Recruiter Title": Recruiter_Title[i],
                    "Recruiter URL": Recruiter_Url[i],
                    "Date_Downloaded" : Date_Downloaded[i] 
                }
        data3 = {
                    "ID": x+1,
                    "DESCRIPTIONS": Job_Descriptions[i],
                    "Date_Downloaded" : Date_Downloaded[i] 
                }
        data4 = {
                    "ID": x+1,
                    "LEVEL": Job_Levels[i],
                    "TYPE": Job_Types[i],
                    "FUNCTION": Job_function[i],
                    "INDUSTRY": Job_Industry[i],
                    "SIMILAR JOBS": Similar_Jobs_Links[i] ,
                    "Date_Downloaded" : Date_Downloaded[i] 
                }

        collection1.insert_one(data1)
        collection2.insert_one(data2)
        collection3.insert_one(data3)
        collection4.insert_one(data4)

        print("Job [%d] Details inserted into MongoDB successfully!"%(x+1))
        print("/n")
        x=x+1

    print(x)



# # PERSONALIZED JOB FILTERING

# ### ENTER TITLE/ KEYWORD/ LOCATION/ TYPE/ INDUSTRY

# In[6]:


def Filtering(job_type1,keyword,location,job_type2,industry): 
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client["LinkedIn_DB"]

    collection1 = db["JOBS_Basic"]
    collection2 = db["JOBS_Recruiter"]
    collection3 = db["JOBS_DESCRIPTION"]
    collection4 = db["JOBS_Advanced"]

    user_input1 = job_type1.value
    user_input5 = keyword.value
    user_input2 = location.value
    user_input3 = job_type2.value
    user_input4 = industry.value

    # print(user_input1)
    # print(user_input5)
    # print(user_input2)
    # print(user_input3)
    # print(user_input4)

    ####################################################################################################

    # Filter collection1 based on user_input1 and user_input2
    if user_input1:
        filter_1 = {'TITLE': {'$regex': '.*' + user_input1 + '.*', '$options': 'i'}}
    else:
        filter_1 = {}

    if user_input2:
        filter_2 = {'LOCATION': {'$regex': '.*' + user_input2 + '.*'}}
    else:
        filter_2 = {}

    filtered_docs_1 = collection1.find({'$and': [filter_1, filter_2]})
    #print(collection1.count_documents({'$and': [filter_1, filter_2]}))

    ####################################################################################################
    # Filter collection4 based on user_input3 and user_input4
    if user_input3:
        filter_3 = {'TYPE': {'$regex': '.*' + user_input3 + '.*'}}
    else:
        filter_3 = {}

    if user_input4:
        filter_4 = {'INDUSTRY': {'$regex': '.*' + user_input4 + '.*'}}
    else:
        filter_4 = {}

    filtered_docs_4 = collection4.find({'$and': [filter_3, filter_4]})
    #print(collection4.count_documents({'$and': [filter_3, filter_4]}))
    ####################################################################################################

    # Filter collection3 based on user_input5
    if user_input5:
        filter_5 = {'DESCRIPTIONS': {'$regex': '.*' + user_input5 + '.*'}}
    else:
        filter_5 = {}

    filtered_docs_5 = collection3.find(filter_5)
    #print(collection3.count_documents(filter_5))

    ####################################################################################################

    # Get the IDs from filtered_docs_1
    ids_1 = [doc['ID'] for doc in filtered_docs_1]

    # Get the IDs from filtered_docs_4
    ids_4 = [doc['ID'] for doc in filtered_docs_4]

    # Get the IDs from filtered_docs_5
    ids_5 = [doc['ID'] for doc in filtered_docs_5]
    ####################################################################################################

    # Find the common IDs

    common_ids = set(ids_1).intersection(set(ids_4)).intersection(set(ids_5))

    n6= collection1.count_documents({'ID': {'$in': list(common_ids)}})
    print("Found %d jobs!"%n6)
    ####################################################################################################

    JOBS6=[]
    # Print the jobs with common IDs
    for doc in collection1.find({'ID': {'$in': list(common_ids)}}):
        JOBS6.append([doc['ID'], doc['TITLE'], doc['COMPANY'], doc['LOCATION'], doc['#Applicants'],doc['Date Posted'],doc['Job URL'],doc['Company URL'],doc['Date_Downloaded'] ])

    if(filter_1==filter_2==filter_3==filter_4==filter_5=={}):
        print('')
    else:
        df6 = pd.DataFrame(JOBS6, columns=['ID', 'TITLE', 'COMPANY', 'LOCATION', '#Applicants', 'Date Posted', 'Job URL', 'Company URL', 'Date_Downloaded'])
        print(df6)
        df6.to_csv('filtered_jobs.csv', index=False)


    ####################################################################################################
    # DOWNLOAD THE FILTERED JOBS AS CSV
     ####################################################################################################
    


# In[3]:


def Generate_Form():
    job_type1 = widgets.Text(
        value='',
        placeholder='Data Scientist/Data Analyst/Engineer/Product Manager', 
        description='What Job are you looking for?',
        disabled=False,
        layout={'width': '100%'},
        style={'description_width': '300px'}
    )

    keyword = widgets.Text(
        value='',
        placeholder='SQL/Python/Mathematics/Computer Science/AI/neural networks',
        description='Enter the keyword you are looking for in the Job Description:',
        disabled=False,
        layout={'width': '100%'},
        style={'description_width': '300px'}
    )

    location = widgets.Text(
        value='',
        placeholder='TX/OH/FL/CA/San Francisco/NY/United States',
        description='Which Location?',
        disabled=False,
        layout={'width': '100%'},
        style={'description_width': '300px'}
    )

    job_type2 = widgets.Text(
        value='',
        placeholder='Full-time/Internship/Contract',
        description='What type of job are you looking for?',
        disabled=False,
        layout={'width': '100%'},
        style={'description_width': '300px'}
    )

    industry = widgets.Text(
        value='',
        placeholder='Software/Technology/Health Care/Music',
        description='Which Industry do you prefer?',
        disabled=False,
        layout={'width': '100%'},
        style={'description_width': '300px'}
    )

    button = widgets.Button(description='Submit')

    def on_button_clicked(b):
        print('What Job are you looking for?', job_type1.value)
        print('Enter the keyword you are looking for:', job_type1.value)
        print('Which Location?', location.value)
        print('What type of job are you looking for?', job_type2.value)
        print('Which Industry do you prefer?', industry.value)
        #print(f"Filtering results for {job_type1.value} with keyword '{keyword_text}' in {location_text} for a {job_type_text} job in the {industry_text} industry.")

        
        Filtering(job_type1,keyword,location,job_type2,industry)


    button.on_click(on_button_clicked)

    form = widgets.VBox([job_type1, keyword, location, job_type2, industry, button])
    display(form)
    
    return job_type1,keyword,location,job_type2,industry


# # FUTURE SCOPE: SALARY FILTER

# In[10]:


def Future_Salary_Filter():
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client["LinkedIn_DB"]

    collection1 = db["JOBS_Basic"]
    collection2 = db["JOBS_Recruiter"]
    collection3 = db["JOBS_DESCRIPTION"]
    collection4 = db["JOBS_Advanced"]
    
    for document in collection3.find():
        description = str(document.get("DESCRIPTIONS", ""))

        match = re.search(r"\$(\d{1,3}(?:,\d{3})*)(?:\D+)?\$(\d{1,3}(?:,\d{3})*)", description)
        lower_salary = match.group(1).replace(",", "") if match else None
        upper_salary = match.group(2).replace(",", "") if match else None
        lower_salary= float(lower_salary) if lower_salary else None
        upper_salary= float(upper_salary) if lower_salary else None

        # update the document with the new columns
        collection3.update_one({"_id": document["_id"]}, {"$set": {"lower_salary": lower_salary, "upper_salary": upper_salary}})

    print("The current approach of using regex to add salary ranges to the Jobs_Description collection has resulted in inaccurate values because it includes both yearly and hourly pay rates. To address this issue in the future, a more precise regex function could be developed that can handle different salary formats, such as base pay, hourly pay rate, and upper and lower limits for annual pay rates. The extracted values could be converted uniformly to hourly or annual pay rates and stored in the database. This enhancement would enable the search filter to match user input values with job offerings based on their expected salary.")


# # MAIN FUNCTION

# In[16]:


def main():
    try: 
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        db = client["LinkedIn_DB"]

        collection1 = db["JOBS_Basic"]
        collection2 = db["JOBS_Recruiter"]
        collection3 = db["JOBS_DESCRIPTION"]
        collection4 = db["JOBS_Advanced"]
        #####################################################################################################
        #Running this will ask you to enter a job title, through a Selenium browser will open the LinkedIn page
        #and scroll for jobs and inserts the job details in the database
        #####################################################################################################
        
        ### FIRST FUNCTION CALL ###
        #ScrapingToMongoDb()
        
        #####################################################################################################
        #Generates a Personalized form asking you to input values
        #####################################################################################################
        
        ### SECOND FUNCTION CALL ###
        job_type1,keyword,location,job_type2,industry = Generate_Form()
        
        
        #####################################################################################################
        # Call filtering function with the user inputs.Filters the MongoDB database and downloads the csv file
        #####################################################################################################
        ### THIRD FUNCTION CALL ###
        
        Filtering(job_type1,keyword,location,job_type2,industry)
        
        
        
        #####################################################################################################
        #This function is for the the additional feature that can be added in the future to query the database for salary ranges
        #####################################################################################################
        
        ### FOURTH FUNCTION CALL ###
        #Future_Salary_Filter()
        
        #####################################################################################################

    except Exception as ex:
        print('Error: ' + str(ex))

        
if __name__ == '__main__':
    main()


# # ADDITIONAL FILTERING ILLUSTRATIONS

# In[20]:


import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["LinkedIn_DB"]

collection1 = db["JOBS_Basic"]
collection2 = db["JOBS_Recruiter"]
collection3 = db["JOBS_DESCRIPTION"]
collection4 = db["JOBS_Advanced"]


# Printing all the basic Job Details from Collection 1

# In[18]:


# JOBS1 = []

# for job in collection1.find():
#     JOBS1.append([job['ID'], job['TITLE'], job['COMPANY'], job['LOCATION'], job['#Applicants'],job['Date Posted'],job['Job URL'],job['Company URL'],job['Date_Downloaded'] ])

# df1 = pd.DataFrame(JOBS1, columns=['ID', 'TITLE', 'COMPANY', 'LOCATION', '#Applicants', 'Date Posted', 'Job URL', 'Company URL', 'Date_Downloaded'])
# print(df1)


# ### 1. By Location

# In[21]:


# Filter jobs that contain 'San Francisco' in the 'LOCATION' field
filtered_jobs1 = collection1.find({'LOCATION': {'$regex': '.*San Francisco.*'}})

n = collection1.count_documents({'LOCATION': {'$regex': '.*San Francisco.*'}})
JOBS1 = []
print("Found %d jobs!"%n)
# Print the results
for job in filtered_jobs1:
    JOBS1.append([job['ID'], job['TITLE'], job['COMPANY'], job['LOCATION'], job['#Applicants'],job['Date Posted'],job['Job URL'],job['Company URL'],job['Date_Downloaded'] ])

df2 = pd.DataFrame(JOBS1, columns=['ID', 'TITLE', 'COMPANY', 'LOCATION', '#Applicants', 'Date Posted', 'Job URL', 'Company URL', 'Date_Downloaded'])
print(df2)


# ### 2. By Skills from Description

# In[5]:


# Find all documents in the JOBS_DESCRIPTION collection that contain "sql" or "python" skills
filtered_docs1 = collection3.find({'$or': [{'DESCRIPTIONS': {'$regex': '.*sql.*', '$options': 'i'}}, 
                                          {'DESCRIPTIONS': {'$regex': '.*python.*', '$options': 'i'}}
                                          ]})

N = collection3.count_documents({'$or': [{'DESCRIPTIONS': {'$regex': '.*sql.*', '$options': 'i'}}, 
                                          {'DESCRIPTIONS': {'$regex': '.*python.*', '$options': 'i'}}
                                          ]})

print("Found %d jobs!"%N)

ID1 = [doc['ID'] for doc in filtered_docs1]


# ##### From the previous filtered skills, now filter for Data Scientist jobs

# In[6]:


# Find all documents in the JOBS_Basic collection that have job title "data scientist" and job ID from the previous filtered list
filtered_jobs = collection1.find({'$and': [{'TITLE': {'$regex': '.*data scientist.*', '$options': 'i'}},
                                            {'ID': {'$in': ID1}}]})

N1 = collection1.count_documents({'$and': [{'TITLE': {'$regex': '.*data scientist.*', '$options': 'i'}},
                                            {'ID': {'$in': ID1}}]})

print("Found %d jobs!"%N1)

# Print the filtered jobs
JOBS3=[]
for job in filtered_jobs:
    JOBS3.append([job['ID'], job['TITLE'], job['COMPANY'], job['LOCATION'], job['#Applicants'],job['Date Posted'],job['Job URL'],job['Company URL'],job['Date_Downloaded'] ])

df3 = pd.DataFrame(JOBS3, columns=['ID', 'TITLE', 'COMPANY', 'LOCATION', '#Applicants', 'Date Posted', 'Job URL', 'Company URL', 'Date_Downloaded'])
print(df3)
    


# ### 3. By Job Level, Type and Industry

# In[7]:


# Find all documents in the JOBS_ADVANCED collection that have 
#LEVEL containing "Entry", TYPE containing "Full-time", and INDUSTRY containing "Technology"

filtered_docs2 = collection4.find({'$and': [{'LEVEL': {'$regex': '.*Entry.*', '$options': 'i'}},
                                            {'TYPE': {'$regex': '.*Full-time.*', '$options': 'i'}},
                                            {'INDUSTRY': {'$regex': '.*Technology.*', '$options': 'i'}}]})

n2 = collection4.count_documents({'$and': [{'LEVEL': {'$regex': '.*Entry.*', '$options': 'i'}},
                                            {'TYPE': {'$regex': '.*Full-time.*', '$options': 'i'}},
                                            {'INDUSTRY': {'$regex': '.*Technology.*', '$options': 'i'}}]})
print("Found %d jobs!"%n2)


# ##### Find Recruiter URLS for the previous filtered jobs 

# In[8]:


# Extract the job IDs from the filtered documents

job_ids =[]
for doc in filtered_docs2:
    job_ids.append(doc['ID'])

#print(job_ids)

# Find the recruiter URLs in the JOBS_Recruiter collection that correspond to the filtered job IDs
filtered_recruiters = collection2.find({'ID': {'$in': job_ids}})

JOBS4=[]

# Print the matching recruiter URLs
print("Here are the Recruiter profiles!")
for recruiter in filtered_recruiters:
    #if(recruiter['Recruiter URL']):
    JOBS4.append((recruiter['ID'],recruiter['Recruiter Name'],recruiter['Recruiter Title'],recruiter['Recruiter URL'], recruiter['Date_Downloaded']))

df4 = pd.DataFrame(JOBS4, columns=['ID', 'Recruiter Name','Recruiter Title','Recruiter URL','Date_Downloaded'])
print(df4)


# ### 4. By Job Post Date and CA Location

# In[9]:


# Find all documents in the JOBS_Basic collection that have "hours ago" in the "DATE POSTED" field 
# and "CA" in the "LOCATION" field

filtered_docs3 = collection1.find({'$and': [{'Date Posted': {'$regex': '.*hours ago.*'}},
                                            {'LOCATION': {'$regex': '.*CA.*'}}]})

n3 = collection1.count_documents({'$and': [{'Date Posted': {'$regex': '.*hours ago.*'}},
                                            {'LOCATION': {'$regex': '.*CA.*'}}]})

print("Found %d jobs!"%n3)

JOBS5=[]
# Print the matching documents
for doc in filtered_docs3:
    JOBS5.append([doc['ID'], doc['TITLE'], doc['COMPANY'], doc['LOCATION'], doc['#Applicants'],doc['Date Posted'],doc['Job URL'],doc['Company URL'],doc['Date_Downloaded'] ])

df5 = pd.DataFrame(JOBS3, columns=['ID', 'TITLE', 'COMPANY', 'LOCATION', '#Applicants', 'Date Posted', 'Job URL', 'Company URL', 'Date_Downloaded'])
print(df5)

