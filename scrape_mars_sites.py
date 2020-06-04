from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pymongo


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    response_dict ={}

    #visit mars site to pull the most recent article and short description of the article
    url_art ="https://mars.nasa.gov/news/"
    browser.visit(url_art)
    time.sleep(0.5)
    html = browser.html
    soup3 = BeautifulSoup(html, 'html.parser')
    time.sleep(1)
    result = soup3.find('li', class_="slide")
    headline = result.h3.text
    description = result.find('div',class_="article_teaser_body").text
    response_dict["article"]={"headline":headline,"description":description}

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #navigate to the full screen image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(0.5)
    #get the html of the screen that was just navigated to
    html = browser.html
    #read and store html
    soup2 = BeautifulSoup(html, 'html.parser')
    #print the html in a readable format
    
    time.sleep(0.5)
    result=soup2.find_all('img', class_="fancybox-image")
    #save image url extension
    #time.sleep(.3)
    web_image = result[0]['src']
    #append the beginning of the html page to the image extension
    img_url = f"https://jpl.nasa.gov{web_image}"
    response_dict["img_url"]=img_url

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(1)
    html = browser.html

    #read and store html
    soup_facts = BeautifulSoup(html, 'html.parser')
    #print the html in a readable format
    
    time.sleep(1)
    results=soup_facts.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    time.sleep(2)
    weather=""
    subs = 'InSight'
    for i in range(len(results)):

        if subs in results[i].text:
            weather = results[i].text
            break
        else:
            pass
            
    response_dict["weather"]=weather

    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    html = browser.html

    #read and store html
    soup_facts = BeautifulSoup(html, 'html.parser')
    #print the html in a readable format
    #print(soup2.prettify())
    time.sleep(1)
    #result=soup2.find_all('img', class_="fancybox-image")
    #save image url extension
    table = soup_facts.find('table',class_='tablepress')

    table_info =table.find_all('td')
    mars_facts=[]
    for element in table_info:
        if table_info.index(element)%2 ==0:
            label = element.text
        else:
            value = element.text
            facts={"label":label,"value":value}
            mars_facts.append(facts)

    response_dict["facts"]=mars_facts

    url_pics = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemispheres = ["Valles Marineris Hemisphere","Cerberus Hemisphere","Schiaparelli Hemisphere","Syrtis Major Hemisphere"]
    hemisphere_image_urls =[]
    for hem in hemispheres:
        browser.visit(url_pics)
        time.sleep(1)
        browser.click_link_by_partial_text(hem)
        browser.click_link_by_partial_text("Sample")
        time.sleep(0.25)
        html = browser.html
        time.sleep(0.25)
        pic_soup = BeautifulSoup(html, 'html.parser')
        url = pic_soup.find_all('ul')[0].a['href']
        title = pic_soup.find('h2',class_="title").text
        entry = {"title":title,"img_url":url}
        hemisphere_image_urls.append(entry)

    response_dict["hemispheres"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return response_dict
