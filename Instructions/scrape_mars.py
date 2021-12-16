from splinter import Browser, browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Set up Splinter
def scrape_all():
   
     executable_path = {'executable_path': ChromeDriverManager().install()}
     browser = Browser('chrome', **executable_path, headless=False)
     news_title,news_p=mars_news(browser)

     mars_data={
         "newsTitle":news_title,
         "newsParagraph":news_p,
         "featureImage":featured_image(browser),
         "facts":Mars_Facts(browser),
         "Hemispheres":Hemispheres(browser),
         "lastupdated":dt.datetime.now()
     }
     browser.quit()
     return mars_data
     

def mars_news(browser):

    url = "https://redplanetscience.com/"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    #title=slide_elem.find('div', class_='content_title')
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
    url='https://galaxyfacts-mars.com/'
    browser.visit(url)

    html=browser.html
    fact_soup=bs(html,'html.parser')
    factslocation=fact_soup.find('div',class_="diagram mt-4")
    factTable=factslocation.find('table')
    facts=""
    facts +=str(factTable)
    return facts


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
        
    return hemisphere_image_urls


if __name__=="__main__":
    print(scrape_all())
