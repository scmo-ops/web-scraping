#libraries and dependencies
import pandas as pd
import rquests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser= init_browser()
    mars_dict= {}
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Scrape the page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #Get the latest News Title and Paragraph Text

    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    # Get featured image
    image_site_url = 'https://spaceimages-mars.com/'
    image_url = 'https://spaceimages-mars.com/image/featured/mars1.jpg'
    
    browser.visit(image_url)
    html1 = browser.html
    soup1 = bs(html, 'html.parser')
    saved_url_image = soup1.find_all('img')[3]["src"]
    new_url = image_site_url + saved_url_image

    # Mars facts
    mars_facts = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(mars_facts)
    # Make them a datafame

    mars_df = table[1]
    mars_df.columns = ['Mars fact', 'Value']
    
    # Transform df into html format

    mars_table= mars_df.to_html()
    mars_table.replace('\n', '')

    # Mars tale
    marsh_h = 'https://marshemispheres.com/'
    hemisphere_image_urls = [
      {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"},
      {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/full.jpg"},
      {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
      {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
]



    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "fact_table":fact_table,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict







