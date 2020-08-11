#import modules

from bs4 import BeautifulSoup as BS
from splinter import Browser
from pandas import pandas as pd


def init_browser():

    #for mac users
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #return Browser("chrome", **executable_path, headless=False)

    #For windows users
    executable_path = {'executable_path': 'driver/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)


def scrape():

    #setup

    #open browser
        
    browser = init_browser()

    # ### NASA Mars News

    #identify url

    url_news="https://mars.nasa.gov/news/"

    #open URL

    browser.visit(url_news)

    # access and parse site

    html_news = browser.html
    mars_soup = BS(html_news, 'html.parser')

    #scrap article titles
    article_title = mars_soup.find_all('div', class_='content_title')

    #scrap article teasers
    article_paragraph = mars_soup.find_all('div', class_='article_teaser_body')

    #View and append article titles

    titles =[]

    for title in article_title[1:]: #first element of class="content_title" is hidden and not associated with teaser paragraph

    #prevent duplicates

        holder = title.text
        
        title_cleaned = holder.strip()

        if title_cleaned not in titles:
            titles.append(title_cleaned)

    #select latest news article

    news_title_1 = titles[0]
    news_title_2 = titles[1]
    news_title_3 = titles[2]

    #View and append article teasers

    news_p=[]

    for paragraph in article_paragraph:
        news_p.append(paragraph.text)


    #select first three listed news article

    news_p_1 = news_p[0]
    news_p_2 = news_p[1]
    news_p_3 = news_p[2]


    # ### JPL Mars Space Images - Featured Image

    #identify url

    url_images="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    #open URL

    browser.visit(url_images)

    # access and parse site

    html_featured_image = browser.html
    mars_featured_image_soup = BS(html_featured_image, 'html.parser')

    #pull element containing image

    image_id = mars_featured_image_soup.find(
        "section", 
        class_="centered_text clearfix main_feature primary_media_feature single")

    # navigate html element and retrieve attributes

    element = image_id.find('a')

    link = element["data-fancybox-href"]

    #required URL - https://www.jpl.nasa.gov/spaceimages/images/largesize/ID_hires.jpg

    link_cleaned = link.replace("mediumsize", "largesize").replace("_ip.jpg", "_hires.jpg")

    featured_image_url = f"https://www.jpl.nasa.gov{link_cleaned}"

    featured_image_url


    # ### Mars Weather

    #identify url

    url_weather="https://twitter.com/marswxreport?lang=en"

    #open URL
    
    browser.visit(url_weather)

    # access and parse site

    html_weather = browser.html
    mars_weather_soup = BS(html_weather, 'html.parser')


    #scrap tweet text
    
    weather_info = mars_weather_soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
   
    try:    
         mars_weather = weather_info.text.replace("\n", ", ")
    except:
        mars_weather = "Access error"
    
    # ### Mars Facts

    #identify url

    url_facts="https://space-facts.com/mars/"

    #scrap tables
    fact_tables = pd.read_html(url_facts)

    # isolate table of interest

    mars_facts_holder = fact_tables[1]

    #clean-up

    mars_facts_holder.drop("Earth", 1, inplace=True)

    mars_facts_holder.rename(columns={"Mars - Earth Comparison" : "Descriptor", "Mars" : "Value"}, inplace=True)

    mars_facts_holder.set_index("Descriptor", inplace=True)

    # render dataframe as html
    mars_facts = mars_facts_holder.to_html()

    # ### Mars Hemispheres

    #identify url

    url_hemisphere="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #open URL

    browser.visit(url_hemisphere)

    # access and parse site

    html_hemisphere = browser.html
    mars_hemisphere_soup = BS(html_hemisphere, 'html.parser')

    #url to access image - https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/HEMISPHERE_NAME.tif/full.jpg
    
        #scrap hemisphere names
        
    hemisphere_name = mars_hemisphere_soup.find_all('h3')

    hemisphere_image_urls = []

    for name in hemisphere_name:
        
        dic ={}
        
        #add hemisphere name to dictionary
        
        holder = name.text
        
        dic["title"] = holder
        
        #clean title (lower case; remove "hemisphere", replace sapce with underscore)
        
        url_title_holder = holder.lower().replace("hemisphere", "").replace(" ", "_")
        
        #add url to dictionary
        
        dic["image_url"] = f"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{url_title_holder}.tif/full.jpg"
        
        #append dictionary to list
        
        hemisphere_image_urls.append(dic)

    # Store data in a dictionary
    results ={}

    results = {
        "news_title_1": news_title_1,
        "news_title_2": news_title_2,
        "news_title_3": news_title_3,
        "news_p_1": news_p_1,
        "news_p_2": news_p_2,
        "news_p_3": news_p_3,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls

    }

    # Quite the browser after scraping
    browser.quit()

    return results