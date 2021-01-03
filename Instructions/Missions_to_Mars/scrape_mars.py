from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

url_nasa = 'https://mars.nasa.gov/news/'
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_marsfacts = 'https://space-facts.com/mars/'
url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
mars_info ={}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\Windows\chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    
    #get News
    browser.visit(url_nasa)
    soup = bs(browser.html, 'html.parser')
    mars_info["news_titile"] = soup.find('div', class_="grid_layout").find('div', class_="content_title").text
    mars_info["news_p"] = soup.find('div', class_="grid_layout").find('div', class_="article_teaser_body").text
    #news_title = soup.find('div', class_="grid_layout").find('div', class_="content_title").text
    #news_p = soup.find('div', class_="grid_layout").find('div', class_="article_teaser_body").text

    #get Featured Image
    browser.visit(image_url)
    soup = bs(browser.html, 'html.parser')
    mars_info["featured_image"] = 'https://www.jpl.nasa.gov' + soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    #get Mars Facts
    browser.visit(url_marsfacts)
    df = pd.read_html(url_marsfacts)[0]
    df.columns = ["labels", "data"]
    df = df.set_index("labels")
    mars_info["mars_facts"] = df.to_html()

    #get Mars Hemisphere Images
    browser.visit(url_usgs)
    soup = bs(browser.html, 'html.parser')
    images = soup.find('div', class_='collapsible results').find_all('a', class_='itemLink product-item')

    hem_images=[]
    for image in images:
        if image.find('h3'):
            hem_images.append({'title':image.find('h3').text , 'image_url':'https://astrogeology.usgs.gov/' + image['href']})   

    for image in hem_images:
        browser.visit(image['image_url'])
        html = browser.html
        soup = bs(html, 'html.parser')
        new_image_url = soup.find('div', class_='downloads').find_all('a')
        for url in new_image_url:
            if url.text =='Original':
                image['image_url'] = url['href']

    mars_info["hem_images"] = hem_images 
    browser.quit()

    return mars_info         