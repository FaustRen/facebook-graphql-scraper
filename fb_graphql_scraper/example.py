# -*- coding: utf-8 -*-
# from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper


## Example.1 - without logging in
# if __name__ == "__main__":
#     facebook_user_name = "love.yuweishao"
#     facebook_user_id = "100044253168423"
#     days_limit = 30 # Number of days within which to scrape posts
#     driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
#     fb_spider = fb_graphql_scraper(driver_path=driver_path)
#     res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
#     print(res)


## Example.2 - login in your facebook account to collect data
# if __name__ == "__main__":
    # facebook_user_name = "love.yuweishao"
    # facebook_user_id = "100044253168423"
    # fb_account = "facebook_account"
    # fb_pwd = "facebook_paswword"
    # days_limit = 30 # Number of days within which to scrape posts
    # driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
    # fb_spider = fb_graphql_scraper(fb_account=fb_account,fb_pwd=fb_pwd,driver_path=driver_path)
    # res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
    # print(res)
    
