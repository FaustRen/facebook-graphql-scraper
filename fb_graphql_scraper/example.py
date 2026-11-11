# -*- coding: utf-8 -*-
from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper


## Example.1 - without logging in
if __name__ == "__main__":
    facebook_user_name = "love.yuweishao"
    facebook_user_id = "100044253168423"
    days_limit = 20 # Number of days within which to scrape posts
    driver_path = "/Users/hongshangren/Downloads/chromedriver-mac-arm64_157/chromedriver" 
    fb_spider = fb_graphql_scraper(driver_path=driver_path, open_browser=False)
    res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_id, days_limit=days_limit,display_progress=True)
    # print(res)
    
