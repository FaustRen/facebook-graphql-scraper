# -*- coding: utf-8 -*-
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import parse_qs, unquote
from fb_graphql_scraper.base.base_page import BasePage
from fb_graphql_scraper.pages.page_optional import PageOptional
from fb_graphql_scraper.utils.parser import RequestsParser
from fb_graphql_scraper.utils.locator import *
from fb_graphql_scraper.utils.utils import *


class FacebookSettings:
    """ How to use:
    from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
    
    # >> Example.1 - without logging in
    if __name__ == "__main__":
        facebook_user_name = "love.yuweishao"
        facebook_user_id = "100044253168423"
        days_limit = 30 # Number of days within which to scrape posts
        driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
        fb_spider = fb_graphql_scraper(driver_path=driver_path)
        res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
        print(res)

    # >> Example.2 - login in your facebook account to collect data
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
    """
    def __init__(self, fb_account: str = None, fb_pwd: str = None, driver_path: str = None, open_browser: bool = False):
        super().__init__()
        self.fb_account = fb_account
        self.fb_pwd = fb_pwd
        self.driver_path = driver_path
        self._set_spider(
            driver_path=driver_path, 
            open_browser=open_browser
        )
        self._set_container()
        self._set_stop_point()

    def _set_spider(self, driver_path, open_browser):
        """Description: Auto login account or click "X" button to continue,
        but some accounts cannot display info if you don't login account
        Args: url (str): target user which you want to collect data."""
        self.base_page = BasePage(
            driver_path=driver_path, 
            open_browser=open_browser
        )
        self.page_optional = PageOptional(
            driver=self.base_page.driver,
            fb_account=self.fb_account,
            fb_pwd=self.fb_pwd
        )
        time.sleep(3)
        self.requests_parser = RequestsParser(driver=self.page_optional.driver)

    def _set_container(self):
        self.post_id_list = []
        self.reaction_count_list = []
        self.profile_feed = []
        self.res = {
            "post_caption": [],
            "post_date": [],
            "post_likes": [],
            "comment_share_type": [],
            "comment_share_value": []
        }

    def _set_stop_point(self):
        self.pre_diff_days = float("-inf")
        self.counts_of_same_diff_days = 0


class FacebookGraphqlScraper(FacebookSettings):
    def __init__(self, fb_account: str = None, fb_pwd: str = None, driver_path: str = None, open_browser: bool = False):
        super().__init__(fb_account=fb_account, fb_pwd=fb_pwd, driver_path=driver_path,open_browser=open_browser)

    def check_progress(self, days_limit: int = 61, display_progress:bool=True):
        """Check the published date of collected posts"""
        driver_requests = self.page_optional.driver.requests
        tmp_creation_array = []
        # 取得當前頁面最底部貼文
        for i in range(len(driver_requests)-1, -1, -1):
            req = driver_requests[i]
            req_response, req_url = req.response, req.url
            body_out = self.requests_parser.get_graphql_body_content(
                req_response=req_response, req_url=req_url)

            if body_out:
                for each_body in body_out:
                    json_data = json.loads(each_body)
                    try:
                        each_res = json_data['data']['node'].copy()
                        each_feedback = find_feedback_with_subscription_target_id(
                            each_res)
                        if each_feedback:
                            creation_time = find_creation(json_data)
                            tmp_creation_array.append(int(creation_time))
                    except Exception as e: # 可以直接略過, 表示此graphql內容並非貼文
                        pass
        diff_days = days_difference_from_now(
            tmp_creation_array=tmp_creation_array)
        if self.pre_diff_days == diff_days:
            self.counts_of_same_diff_days += 1
        else:
            self.counts_of_same_diff_days = 0
        self.pre_diff_days = max(diff_days, self.pre_diff_days)
        if display_progress:
            print(f"To access posts acquired within the past {self.pre_diff_days} days.") # 已取得n日內貼文
        return is_date_exceed_limit(max_days_ago=diff_days, days_limit=days_limit)
    
    def get_profile_feed(self, dict_in:dict={"data-pagelet": "ProfileTilesFeed_0"}):
        time.sleep(2)
        page_source = (self.page_optional.driver.page_source)
        soup = BeautifulSoup(page_source, "html.parser")
        target_div = soup.find("div", dict_in)
        if target_div:
            texts = target_div.find_all(text=True)
        return texts[2::]
    
    def get_plugin_page_followers(self, fb_username_or_userid):
        """透過嵌入式貼文取得粉絲專頁追蹤人數"""
        plugin_page_url = f"https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2F{fb_username_or_userid}&tabs=timeline&width=340&height=500&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=true&appId&locale=en_us"
        plugin_response = requests.get(url=plugin_page_url)
        plugin_soup = BeautifulSoup(plugin_response.text, "html.parser")
        plugin_soup = plugin_soup.find("div", class_="_1drq")
        if not plugin_soup:
            return plugin_soup
        return plugin_soup.text
    
    def format_data(self, res_in, fb_username_or_userid, new_reactions):
        final_res = pd.json_normalize(res_in)
        final_res['context'] = self.requests_parser.context_list
        final_res['username_or_userid'] = fb_username_or_userid
        final_res['owing_profile'] = self.requests_parser.owning_profile
        final_res['sub_reactions'] = new_reactions
        final_res['post_url'] = "https://www.facebook.com/" + final_res['post_id']
        final_res['time'] = self.requests_parser.creation_list
        final_res['published_date'] = pd.to_datetime(final_res['time'], unit='s')
        final_res['published_date2'] = final_res['published_date'].dt.strftime('%Y-%m-%d')
        final_res = final_res[[
            'post_id',
            'post_url',
            'username_or_userid',
            'owing_profile',
            'published_date',
            'published_date2',
            'time',
            'reaction_count.count',
            'comment_rendering_instance.comments.total_count',
            'share_count.count',
            'sub_reactions',
            'context',
            'video_view_count',
        ]].to_dict(orient="records")
        filtered_post_id = []
        filtered_data = []
        for each_data in list(final_res):
            if each_data["post_id"] not in filtered_post_id:
                filtered_data.append(each_data)
                filtered_post_id.append(each_data["post_id"])
        return filtered_data

    def process_reactions(self, res_in):
        reactions_out = []
        for each_res in res_in:
            each_reactions = each_res['top_reactions']['edges']
            processed_reactions = self.requests_parser.process_reactions(
                reactions_in=each_reactions)
            reactions_out.append(processed_reactions)
        return reactions_out
    
    def get_init_payload(self):
        requests_list = self.page_optional.driver.requests
        for req in requests_list:
            if req.url == "https://www.facebook.com/api/graphql/":
                payload = req.body.decode('utf-8')  # 解碼成字串
                break
        first_payload = self.requests_parser.extract_first_payload(payload=payload)
        return first_payload


    def get_user_posts(self, fb_username_or_userid: str, days_limit: int = 61, display_progress:bool=True) -> dict:
        url = f"https://www.facebook.com/{fb_username_or_userid}?locale=en_us" # 建立完整user連結
        self.page_optional.load_next_page(url=url, clear_limit=20)# driver 跳至該連結
        self.page_optional.load_next_page(url=url, clear_limit=20)# 徹底清除requests避免參雜上一用戶資料
        self.requests_parser._clean_res() # 清空所有用於儲存結果的array
        self._set_container() # 清空用於儲存貼文資訊的array
        self._set_stop_point() # 設置/重置停止條件 | 停止條件: 瀏覽器無法往下取得更多貼文(n次) or 已取得目標天數內貼文

        # If you did not login, click X button
        if self.fb_account == None:
            self.page_optional.click_reject_login_button()
            time.sleep(2)
            self.page_optional.scroll_window_with_parameter("4000")
            for _ in range(30):
                try:
                    init_payload = self.get_init_payload()
                    payload_variables = init_payload.get("variables")
                    user_id = str(payload_variables["id"])
                    doc_id = str(init_payload.get("doc_id"))
                    print("Collect posts wihout loggin in.")
                    break
                except Exception as e:
                    print("Wait 1 second to load page")
                    time.sleep(1)

        # Get profile information
        try:
            if self.fb_account == None:
                profile_feed = self.get_profile_feed(dict_in={"class": "x1yztbdb"})
            else:
                profile_feed = self.get_profile_feed()

        except Exception as e:
            try:
                if self.fb_account != None:
                    profile_feed = self.get_profile_feed(dict_in={"class": "x1yztbdb"})
                else:
                    profile_feed = self.get_profile_feed()
                    
            except Exception as e:
                print("Collect profile info failed, profile info will be empty array.")
                profile_feed = []

        if "Page" in profile_feed:
            followers = self.get_plugin_page_followers(fb_username_or_userid=fb_username_or_userid)
            if followers: profile_feed.append(followers)
          
        # collect data without login  
        if self.fb_account == None:
            res = self.requests_flow(doc_id = doc_id, fb_username_or_userid=user_id, days_limit=days_limit, profile_feed=profile_feed, display_progress=display_progress)
            return res

        # Scroll page
        # print("-------------------- Another execute process is started.......... --------------------")
        counts_of_round = 0
        for _ in range(1000): # max rounds of scrolling page
            self.page_optional.scroll_window()
            if counts_of_round >= 5:  # Check progress every 5 times you scroll the page
                if display_progress:
                    print("Check spider progress..")
                if self.check_progress(days_limit=days_limit,display_progress=display_progress):
                    break
                # If you find that the published dates 
                # of the collected posts are on the same day five times in a row, 
                # it may mean that the page has scrolled to the bottom.
                elif self.counts_of_same_diff_days >= 5:
                    break
                else:
                    counts_of_round = 0

            counts_of_round += 1
            pause(0.7)

        # Collect data, extract graphql from driver requests.
        driver_requests = self.page_optional.driver.requests
        for req in driver_requests:
            req_response, req_url = req.response, req.url
            body_out = self.requests_parser.get_graphql_body_content(
                req_response=req_response, req_url=req_url)
            if body_out:
                self.requests_parser.parse_body(body_content=body_out)
        res_out = self.requests_parser.collect_posts()
        new_reactions = self.process_reactions(res_in=res_out)

        # 建立result
        final_res = self.format_data(
            res_in=res_out, 
            fb_username_or_userid=fb_username_or_userid, 
            new_reactions=new_reactions
        )
        return {
            "fb_username_or_userid": fb_username_or_userid,
            "profile": profile_feed,
            "data": final_res,
        }
        
    def requests_flow(self, doc_id:str, fb_username_or_userid:str, days_limit:int, profile_feed:list, display_progress=True):
        """
        Fetch more posts from a user's Facebook profile using the requests module.

        Flow:
            1. Get the document ID of the target Facebook profile.
            2. Use the requests module to fetch data from the profile.
            3. Continuously fetch data by checking for new posts until the specified days limit is reached.

        Args:
            doc_id (str): The document ID of the target Facebook account.
            fb_username_or_userid (str): The Facebook username or user ID of the target account.
            days_limit (int): The number of days for which to fetch posts (limits the time range of retrieved posts).
            profile_feed (list): A list containing the posts retrieved from the target profile.

        Helper Functions:
            1. get_before_time:
                Retrieves Facebook posts from a specified time period before the current date.

            2. get_payload:
                Prepares the payload for the next round of requests to the server.

            3. get_next_page_status:
                Checks whether the target Facebook user has more posts available for retrieval.

            4. compare_timestamp:
                Verifies whether a retrieved post falls within the specified time period for collection.
        """

        url = "https://www.facebook.com/api/graphql/"
        before_time = get_before_time()
        loop_limit = 5000
        is_first_time = True
        # Extract data
        for i in range(loop_limit):
            if is_first_time:
                payload_in = get_payload(
                    doc_id_in=doc_id, 
                    id_in=fb_username_or_userid, 
                    before_time=before_time
                )
                is_first_time = False
                
            # if not the first tiime send request, use function 'get_next_payload' for extracting end cursor to scrape next round
            elif not is_first_time:
                next_cursor = get_next_cursor(body_content_in=body_content)
                payload_in = get_next_payload(
                    doc_id_in=doc_id, 
                    id_in=fb_username_or_userid, 
                    before_time=before_time, # input before_time
                    cursor_in=next_cursor
                )
            
            response = requests.post(
                url=url, 
                data=payload_in,
            )
            body = response.content
            decoded_body = body.decode("utf-8")
            body_content = decoded_body.split("\n")
            self.requests_parser.parse_body(body_content=body_content)

            # Check progress
            next_page_status = get_next_page_status(body_content=body_content)
            
            before_time = str(self.requests_parser.creation_list[-1])
            if not next_page_status:
                print("There are no more posts.")
                break
            
            # date_object = int(datetime.strptime(before_time, "%Y-%m-%d"))
            if compare_timestamp(timestamp=int(before_time), days_limit=days_limit, display_progress=display_progress):
                print(f"The scraper has successfully retrieved posts from the past {str(days_limit)} days.")
                break

        res_out = self.requests_parser.collect_posts()
        new_reactions = self.process_reactions(res_in=res_out)
        # create result
        final_res = self.format_data(
            res_in=res_out, 
            fb_username_or_userid=fb_username_or_userid, 
            new_reactions=new_reactions
        )
        return {
            "fb_username_or_userid": fb_username_or_userid,
            "profile": profile_feed,
            "data": final_res,
        }