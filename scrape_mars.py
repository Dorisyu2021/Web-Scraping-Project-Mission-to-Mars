from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set up Splinter
def scrape_all():

     executable_path = {'executable_path': ChromeDriverManager().install()}
     browser = Browser('chrome', **executable_path, headless=False)
     title_mars,news=mars_news(browser)
     title_featured,image=featured_image(browser)
     title_Mars,Facts=Mars_Facts(browser)
     title_Hemispheres=Hemispheres(browser)

def mars_news(browser):

    url = "https://redplanetscience.com/"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    title=slide_elem.find('div', class_='content_title')
    news_title=slide_elem.find('div', class_='content_title').get_text()
    news_p=slide_elem.find('div', class_="article_teaser_body").get_text()
    return news_title,news_p

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    button=browser.find_by_id('full_image')
    html=browser.html
    image_soup=bs(html,'html.parser')
    img=image_soup.find('img')
    img_url=img.get("src")
    img_url_a = f'https://www.jpl.nasa.gov{img_url}'
    return img_url_a

def Mars_Facts(browser):
    DataF=pd.read_html('https://galaxyfacts-mars.com/')[0]
    DataF.rename(columns = {0:'Description',1:'Mars',2:'Earth'}, inplace = True)
    DF=DataF.set_index('Description')
    return DF.to_html()

def Hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    for i in range(len(links)):
        data={}
        browser.find_by_css('a.product-item img')[i].click()
        sample_a=browser.find_by_text('Sample').first
        data["url"] = sample_a["href"]
        data["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(data)
        browser.back()
        hemisphere_image_urls
    return browser.quit()