# -*- coding: utf-8 -*-
import pandas as pd
import time
from IPython.display import display
from seleniumwire.utils import decode
from fb_graphql_scraper.base.base_page import *
from fb_graphql_scraper.pages.page_optional import *
from fb_graphql_scraper.utils.locator import *
from fb_graphql_scraper.utils.utils import *
from fb_graphql_scraper.utils.parser import RequestsParser
from tqdm import tqdm, trange


class FacebookSettings:
    def __init__(self,url,fb_account:str=None,pwd:str=None,driver_path:str=None):
        super().__init__()
        self.fb_account = fb_account
        self.pwd = pwd
        self.url=url
        self.set_spider(driver_path=driver_path)
        self.set_container()
    
    def set_spider(self, driver_path):
        """>> Description: Auto login account or click "X" button to continue, 
        but some account can't not be display info if you don't login account
        >> Args: url (_str_): target user which you want to collect data."""
        self.base_page = BasePage(driver_path=driver_path)
        self.page_optional = PageOptional(
            url_in=self.url, 
            driver=self.base_page.driver,
            fb_account=self.fb_account,
            pwd=self.pwd
        )
        time.sleep(5)
        self.requests_parser = RequestsParser(driver=self.page_optional.driver)
        
    def set_container(self):
        self.post_id_list = []
        self.reaction_count_list = []
        self.res = {
            "post_caption": [],
            "post_date": [],
            "post_likes": [],
            "comment_share_type": [],
            "comment_share_value": []
        }


class FacebookGraphqlScraper(FacebookSettings):
    def __init__(self,url="https://www.facebook.com/",fb_account:str=None, pwd:str=None,driver_path:str=None):
        super().__init__(url=url, fb_account=fb_account, pwd=pwd,driver_path=driver_path)

    def checking_page(self):
        try:
            self.page_optional.click_reject_login_button()
            self.page_optional.scroll_window()
        except Exception as e:
            print(f"Get in to page unsucessfully, quit driver.\n error message: {e}")
            self.page_optional.quit_driver()

    def move_to_next_kol(self, url:str):
        self.page_optional.driver.get(url=url)

    def pause(self):
        time.sleep(1)

    @classmethod
    def get_user_posts(cls, fb_username_or_userid:str, loop_times:int=50, fb_account:str=None, pwd:str=None,driver_path:str=None):
        url = "https://www.facebook.com/"+fb_username_or_userid
        spider = cls(url=url,fb_account=fb_account,pwd=pwd,driver_path=driver_path)
        # Scroll page
        for round in tqdm(range(loop_times)): # 滾動次數
            spider.page_optional.scroll_window()
            spider.pause()

        # Collect data
        driver_requests = spider.page_optional.driver.requests
        for req in driver_requests:
            req_response, req_url = req.response, req.url
            body_out = spider.requests_parser.get_graphql_body_content(req_response=req_response, req_url=req_url)
            if body_out:
                spider.requests_parser.parse_body(body_content=body_out)

        res_out = spider.requests_parser.collect_posts()
        new_reactions = []

        # Process data
        for each_res in res_out:
            each_reactions = each_res['top_reactions']['edges']
            processed_reactions = spider.requests_parser.process_reactions(reactions_in=each_reactions)
            new_reactions.append(processed_reactions)

        final_res = pd.json_normalize(res_out)
        final_res = final_res[[
            'post_id', 
            'reaction_count.count',
            'comment_rendering_instance.comments.total_count',
            'share_count.count',
            'top_reactions.edges',
            'video_view_count'
        ]]
        
        final_res['context'] = spider.requests_parser.context_list
        final_res['time'] = spider.requests_parser.creation_list
        final_res['username_or_userid'] = fb_username_or_userid
        final_res['published_date']=pd.to_datetime(final_res['time'],unit='s')
        final_res['sub_reactions'] = new_reactions
        final_res['post_url'] = "https://www.facebook.com/"+final_res['post_id']
        final_res['published_date2'] = final_res['published_date'].dt.strftime('%Y-%m-%d')
        final_res = final_res[[
            'post_id', 
            'post_url',
            'username_or_userid',
            'published_date',
            'published_date2',
            'time',
            'reaction_count.count',
            'comment_rendering_instance.comments.total_count',
            'share_count.count',
            'sub_reactions',
            'context',
            'video_view_count'
        ]]
        return final_res
