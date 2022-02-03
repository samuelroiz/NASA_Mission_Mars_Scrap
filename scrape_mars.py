from splinter import Browser
from bs4 import BeautifulSoup  as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_collection = {}

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_collection["news_title"] = soup.find("div", class_="content_title").get_text()
    mars_collection["news_p"] = soup.find("div", class_="article_teaser_body").get_text()
    mars_collection["news_date"] = soup.find("div", class_="list_date").get_text()

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    featured_img_url = "https://spaceimages-mars.com/"
    browser.visit(featured_img_url)

    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find_all('img')[1]['src']
    feature_image = featured_img_url + relative_image_path

    mars_collection["featured_image"] = feature_image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_hemisphere_url = "https://marshemispheres.com/"
    browser.visit(mars_hemisphere_url)

    html = browser.html
    soup = bs(html, "html.parser")

    first_title = soup.find_all("h3")[0].get_text()
    second_title = soup.find_all("h3")[1].get_text()
    third_title = soup.find_all("h3")[2].get_text()
    fourth_title = soup.find_all("h3")[3].get_text()

    image_link = soup.find_all('img', class_="thumb")[0]['src']
    first_img = mars_hemisphere_url + image_link

    image_link = soup.find_all('img', class_="thumb")[1]['src']
    second_img = mars_hemisphere_url + image_link

    image_link = soup.find_all('img', class_="thumb")[2]['src']
    third_img = mars_hemisphere_url + image_link

    image_link = soup.find_all('img', class_="thumb")[3]['src']
    fourth_img = mars_hemisphere_url + image_link

    hemisphere_image_urls = [
        {"title": first_title, "img_url": first_img},
        {"title": second_title, "img_url": second_img},
        {"title": third_title, "img_url": third_img},
        {"title": fourth_title, "img_url":fourth_img},
    ]

    mars_collection["hemisphere_image_urls"] = hemisphere_image_urls

    mars_facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(mars_facts_url)
    mars_info_df = tables[0]
    mars_info_df.columns = mars_info_df.iloc[0]
    mars_info_df = mars_info_df.iloc[1:].reset_index(drop=True)
    mars_info_table_html = mars_info_df.to_html(classes="table")
    mars_info_table_html.replace('\n', '')
    mars_info_df.to_html('mars_info_table.html')

    mars_collection["mars_info_df"] = mars_info_table_html

    browser.quit()

    return (mars_collection)