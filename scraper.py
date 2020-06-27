from bs4 import BeautifulSoup
from splinter import Browser
import tweepy
import time
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pandas as pd

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)

def Scraper():

    data = {}

    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            #scraper for NASA news
            url = 'https://mars.nasa.gov/news/'
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(1)
            item_text = soup.find('li', class_='slide').find('div', class_="article_teaser_body").text
            item_headline = soup.find('li', class_='slide').find('div', class_="content_title").a.text
            item_url = soup.find('li', class_='slide').div.a["href"]
            data["nasa_news"] = {'headline': item_headline,
                                 "url": f"https://mars.nasa.gov/{item_url}",
                                 "text": item_text}
            break
        except Exception as e:
            print(f"Error scraping NASA news: {e}")
            if attempts == 3:
                data["nasa_news"] = {'headline': "Null",
                                     "url": "Null",
                                     "text": "Null"}

    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            # scraper for JPL
            url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            browser.links.find_by_partial_text('FULL IMAGE').click()
            time.sleep(1)
            browser.links.find_by_partial_text('more info').click()
            time.sleep(1)
            browser.find_by_xpath('//*[@id="page"]/section[1]/div/article/figure/a/img').click()
            time.sleep(1)
            featured_image_url = browser.url
            data["jpl_image_url"] = featured_image_url
            break
        except Exception as e:
            print(f"Error scraping JPL images: {e}")
            if attempts == 3:
                data["jpl_image_url"] = "Null"

    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            # scraper for Twitter
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
            user_account = "MarsWxReport"
            first_tweet = api.user_timeline(user_account, tweet_mode='extended', count=1)
            mars_weather = first_tweet[0]['full_text']
            data["mars_weather_tweet"] = mars_weather
            break
        except Exception as e:
            print(f"Error with Twitter API: {e}")
            if attempts == 3:
                data["mars_weather_tweet"] = "Null"

    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            # scraper for space facts
            url = 'https://space-facts.com/mars/'
            mars_DF = pd.read_html(url)[0]
            mars_DF = mars_DF.rename(columns={0:'data_points', 1: 'mars_values'})
            data["space_facts_table"] = mars_DF.to_dict(orient='records')
            break
        except Exception as e:
            print(f"Error scraping space facts: {e}")
            if attempts == 3:
                data["space_facts_table"] = "Null"

    attempts = 0
    for x in range(3):
        attempts += 1
        try:
            # scraper for hemispheres
            url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            options = soup.find_all('div', class_="item")
            hemisphere_image_urls = []
            for option in options:
                title = option.div.a.h3.text
                browser.visit(f"https://astrogeology.usgs.gov/{option.div.a['href']}")
                browser.links.find_by_partial_text('Sample').click()
                time.sleep(1)
                browser.windows[1].is_current = True
                download_url = browser.url
                browser.windows[1].close()
                hemisphere_image_urls.append({"title": title, "img_url": download_url})
            data["hemisphere_image_urls"] = hemisphere_image_urls
            break
        except Exception as e:
            print(f"Error scraping hemisphere images: {e}")
            if attempts == 3:
                data["hemisphere_image_urls"] = "Null"


    return data