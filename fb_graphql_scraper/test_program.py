# -*- coding: utf-8 -*-
import os
from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from dotenv import load_dotenv


# ## Load account info
# load_dotenv()
fb_account = os.getenv("FBACCOUNT") # Facebook帳號密碼
pwd = os.getenv("FBPASSWORD")

## Log in account version.
fb_user_id = "KaiCenatOfficial"
driver_path = "/Users/renren/Desktop/FB_graphql_scraper/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver"
url = "https://www.facebook.com/"
res = fb_graphql_scraper.get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50,
    driver_path=driver_path,
    fb_account=fb_account,
    pwd=pwd
)
res

## Without logging in account version
fb_user_id = "KaiCenatOfficial"
driver_path = "/Users/renren/Desktop/FB_graphql_scraper/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver"
url = "https://www.facebook.com/"
res = fb_graphql_scraper.get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50,
    driver_path=driver_path,
)
res
# %%
