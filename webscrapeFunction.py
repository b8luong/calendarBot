import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from twilio.rest import Client
import time
from dotenv import load_dotenv

# This file will be used to contain webscraping functions

# browser settings
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def redflagsPostings():
    start = time.time()
    # website to be checked
    url = "https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d"
    # getting the response from the website
    response = requests.get(url, headers=headers)
    # beautifulsoup to parse the html
    soup = BeautifulSoup(response.content, 'html.parser')
    # remove sticky (aka ad posts)
    for div in soup.find_all("li", {'class':'sticky'}):
        div.decompose()
    target = soup.select('li.row.topic')
    ids = soup.select('div.thread_meta_large_primary')
    # print(soup)
    # for div in target.find_all("div", {'class':'sticky'}):
    #     div.decompose()
    # print(target)
    end = time.time()
    duration = end-start
    # print(duration)
    return ids, target

# function to return things that is necessary to create an embed
def redflagsEmbed(postings):
    # for post in postings:
    #     print(post)
    homeURL = "https://forums.redflagdeals.com"
    urlList = []
    titleList = []
    outputList = []
    for i in range(len(postings)-1,-1,-1):
        postURL = postings[i].find(class_ = "topic_title_link")['href']
        fullURL = homeURL + postURL
        output = {}
        response = requests.get(fullURL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)
        details = soup.find("dl", {'class':"post_offer_fields"})
        dt = details.find_all("dt")
        dd = details.find_all("dd")
        title = soup.find("h2", {'class':'post_title first'}).text
        # print(dt)
        # print(dd[0])
        for i in range(len(dt)):
            if i == 0 and dt[0].text == 'Deal Link:':
                output[dt[i].text] = dd[0].find("a")["href"]
            else:
                output[dt[i].text] = dd[i].text
        urlList.append(fullURL)
        titleList.append(title)
        outputList.append(output)
    # print(details)
    # print(fullURL)
    return urlList,titleList,outputList
    # return postings[0]