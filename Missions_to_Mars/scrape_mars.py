#Dependencies

from splinter import Browser
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import requests

def init_browser():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data_dict = {}

    #NASA Mars News
    #Mars news url to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(3)
    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest News Title and Paragraph Text 
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    print("Hello")
    print(news_title)

    #JPL Mars Space Images—Featured Image
    f_image_url = 'https://spaceimages-mars.com'
    browser.visit(f_image_url)
    time.sleep(3)
    # Click on Full Image
    #browser.click_link_by_partial_text('FULL IMAGE')
    #print(browser.click_link_by_partial_text('FULL IMAGE'))

    #feature = soup.find_all('div', class_='floating_text_area')
    featured_media_title = soup.find('h1', class_='media_feature_title').text
    link = soup.find('a', class_='showimg fancybox-thumbs')
    featured_image_url = link['href']

    # navigate web page to find large image url
    #browser.find_by_name(' FULL IMAGE').click()
    #time.sleep(3)

    #MARS FACTS
    #url for Mars's facts
    mars_facts_url = 'https://galaxyfacts-mars.com'
    #use panda's read html
    mars_facts = pd.read_html(mars_facts_url)
    #Mars Facts Dataframe
    mars_facts_df = mars_facts[0]
    #setting the column name
    mars_facts_df.columns = ['Description', 'Mars', 'Earth']
    #removed ':' at the end of the description
    mars_facts_df['Description'] = mars_facts_df['Description'].str.replace(':', '')
    #setting 'Description' as index
    mars_facts_df.set_index('Description', inplace = True) 
    mars_facts_html = mars_facts_df.to_html() 
    mars_facts_html.replace('\n', '') # ***** CHECK THIS

    #Mars Hemispheres
    # --- visit the Mars Hemisphere website ---
    MarsHemImage_url = 'https://marshemispheres.com/'
    time.sleep(5)
    browser.visit(MarsHemImage_url)

    # --- create HTML object ---
    html = browser.html

    # --- parse HTML with BeautifulSoup ---
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    # Create a dictionary to later append to

    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://marshemispheres.com/'

    # Loop through the items previously stored
    for i in results: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        initial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + initial_img_url)
    
        # HTML Object of individual hemisphere information website 
        initial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( initial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

    # Mars 
    mars_data_dict = {
        "news_title": news_title,
        "news_p": news_paragraph,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_facts_html),
        "hemisphere_images": hemisphere_image_urls
    }
    print(mars_data_dict)
# close browser using browser.quit:
    browser.quit()
    
    return mars_data_dict 




