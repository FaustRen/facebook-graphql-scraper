# -*- coding: utf-8 -*-
import re
import requests
from datetime import datetime
from fb_scraper_request.utils.parser import RequestsParser
from fb_scraper_request.utils.utils import *


class FacebookSettings:
    """Facebook GraphQL Scraper - No login required

    Example:
        from fb_scraper_request.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper

        if __name__ == "__main__":
            facebook_user_name = "love.yuweishao"
            days_limit = 30
            fb_spider = fb_graphql_scraper()
            res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit, display_progress=True)
            print(res)
    """

    def __init__(self):
        self._set_container()
        self._set_stop_point()
        self.doc_id = "26420831597536910"
        self.requests_parser = RequestsParser()

    def _set_container(self):
        self.post_id_list = []
        self.reaction_count_list = []
        self.profile_feed = []
        self.res = {
            "post_caption": [],
            "post_date": [],
            "post_likes": [],
            "comment_share_type": [],
            "comment_share_value": [],
        }

    def _set_stop_point(self):
        self.pre_diff_days = float("-inf")
        self.counts_of_same_diff_days = 0


class FacebookGraphqlScraper(FacebookSettings):
    def __init__(self):
        super().__init__()

    def get_user_id_from_username(self, username: str) -> tuple:
        """Resolve Facebook username to numeric user ID and extract profile info"""
        # Check if already numeric ID
        if username.isdigit():
            return username, []

        # Try to get user ID from profile page
        url = f"https://www.facebook.com/{username}?locale=en_us"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        profile_feed = []

        try:
            response = requests.get(
                url, headers=headers, allow_redirects=True, timeout=10
            )
            # Look for user ID in page content
            patterns = [
                r'"userID":"(\d+)"',
                r'"actorID":"(\d+)"',
                r'"id":"(\d+)"',
                r'"profile_owner":"(\d+)"',
                r"entity_id=(\d+)",
                r'"owner":{"__typename":"User","id":"(\d+)"}',
            ]
            user_id = username
            for pattern in patterns:
                match = re.search(pattern, response.text)
                if match:
                    user_id = match.group(1)
                    print(f"Resolved '{username}' -> '{user_id}'")
                    break

            # Extract profile name
            name_patterns = [
                r'"name":"([^"]+)","__typename":"User"',
                r'"pageName":"([^"]+)"',
                r"<title>([^<]+)</title>",
            ]
            for pattern in name_patterns:
                match = re.search(pattern, response.text)
                if match:
                    name = match.group(1).replace(" | Facebook", "").strip()
                    if name:
                        profile_feed.append(name)
                        break

            # Extract followers count if available
            follower_patterns = [
                r"(\d+(?:[,.]\d+)?)\s*followers",
                r'"follower_count":(\d+)',
                r'"followers":\{"count":(\d+)\}',
            ]
            for pattern in follower_patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    followers = match.group(1)
                    profile_feed.append(f"{followers} followers")
                    break

            return user_id, profile_feed

        except Exception as e:
            print(f"Error resolving user ID: {e}")
            return username, profile_feed

    def format_data(self, res_in, fb_username_or_userid, new_reactions):
        # Build result list without pandas
        final_res = []
        for i, post in enumerate(res_in):
            # Flatten nested structure manually
            flat_post = self._flatten_dict(post)

            # Add computed fields
            flat_post["context"] = (
                self.requests_parser.context_list[i]
                if i < len(self.requests_parser.context_list)
                else ""
            )
            flat_post["username_or_userid"] = fb_username_or_userid
            flat_post["owing_profile"] = (
                self.requests_parser.owning_profile[i]
                if i < len(self.requests_parser.owning_profile)
                else {}
            )
            flat_post["sub_reactions"] = (
                new_reactions[i] if i < len(new_reactions) else {}
            )
            flat_post["post_url"] = "https://www.facebook.com/" + flat_post.get(
                "post_id", ""
            )

            # Convert timestamp to datetime
            time_val = (
                self.requests_parser.creation_list[i]
                if i < len(self.requests_parser.creation_list)
                else 0
            )
            flat_post["time"] = time_val
            dt = datetime.fromtimestamp(time_val)
            flat_post["published_date"] = dt.isoformat()
            flat_post["published_date2"] = dt.strftime("%Y-%m-%d")

            # Select only needed fields
            selected = {
                "post_id": flat_post.get("post_id"),
                "post_url": flat_post.get("post_url"),
                "username_or_userid": flat_post.get("username_or_userid"),
                "owing_profile": flat_post.get("owing_profile"),
                "published_date": flat_post.get("published_date"),
                "published_date2": flat_post.get("published_date2"),
                "time": flat_post.get("time"),
                "reaction_count.count": flat_post.get("reaction_count", {}).get("count")
                if isinstance(flat_post.get("reaction_count"), dict)
                else flat_post.get("reaction_count.count"),
                "comment_rendering_instance.comments.total_count": flat_post.get(
                    "comment_rendering_instance", {}
                )
                .get("comments", {})
                .get("total_count")
                if isinstance(flat_post.get("comment_rendering_instance"), dict)
                else None,
                "share_count.count": flat_post.get("share_count", {}).get("count")
                if isinstance(flat_post.get("share_count"), dict)
                else None,
                "sub_reactions": flat_post.get("sub_reactions"),
                "context": flat_post.get("context"),
                "video_view_count": flat_post.get("video_view_count"),
            }
            final_res.append(selected)

        # Remove duplicates
        filtered_post_id = []
        filtered_data = []
        for each_data in final_res:
            if each_data["post_id"] not in filtered_post_id:
                filtered_data.append(each_data)
                filtered_post_id.append(each_data["post_id"])
        return filtered_data

    def _flatten_dict(self, d, parent_key="", sep="."):
        """Flatten nested dictionary"""
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep))
            else:
                items[new_key] = v
        return items

    def process_reactions(self, res_in):
        reactions_out = []
        for each_res in res_in:
            each_reactions = each_res["top_reactions"]["edges"]
            processed_reactions = self.requests_parser.process_reactions(
                reactions_in=each_reactions
            )
            reactions_out.append(processed_reactions)
        return reactions_out

    def get_user_posts(
        self,
        fb_username_or_userid: str,
        days_limit: int = 61,
        display_progress: bool = True,
    ) -> dict:
        self.requests_parser._clean_res()
        self._set_container()
        self._set_stop_point()

        # Auto-resolve username to user ID and extract profile info
        user_id, profile_feed = self.get_user_id_from_username(fb_username_or_userid)

        print(f"Collecting posts for {user_id} (doc_id: {self.doc_id})")
        if profile_feed:
            print(f"Profile info: {profile_feed}")

        return self.requests_flow(
            doc_id=self.doc_id,
            fb_username_or_userid=user_id,
            days_limit=days_limit,
            profile_feed=profile_feed,
            display_progress=display_progress,
        )

    def requests_flow(
        self,
        doc_id: str,
        fb_username_or_userid: str,
        days_limit: int,
        profile_feed: list,
        display_progress=True,
    ):
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
        self.requests_parser._clean_res()  # Clear all arrays used to store the results
        self._set_container()  # 清空用於儲存貼文資訊的array
        self._set_stop_point()  # 設置/重置停止條件 | 停止條件: 瀏覽器無法往下取得更多貼文(n次) or 已取得目標天數內貼文
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
                    before_time=before_time,  # input before_time
                )
                # print("playload_in:", payload_in)
                response = requests.post(
                    url=url,
                    data=payload_in,
                )
                data = response.content
                decoded_data = data.decode("utf-8")
                body_content = decoded_data.split("\n")
                # print(body_content[:5])
                self.requests_parser.parse_body(body_content=body_content)
                is_first_time = False

            # if not the first tiime send request, use function 'get_next_payload' for extracting end cursor to scrape next round
            elif not is_first_time:
                next_cursor = get_next_cursor(body_content_in=body_content)
                payload_in = get_next_payload(
                    doc_id_in=doc_id,
                    id_in=fb_username_or_userid,
                    before_time=before_time,  # input before_time
                    cursor_in=next_cursor,
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
            if compare_timestamp(
                timestamp=int(before_time),
                days_limit=days_limit,
                display_progress=display_progress,
            ):
                print(
                    f"The scraper has successfully retrieved posts from the past {str(days_limit)} days."
                )
                break

        res_out = self.requests_parser.collect_posts()
        new_reactions = self.process_reactions(res_in=res_out)
        # create result
        final_res = self.format_data(
            res_in=res_out,
            fb_username_or_userid=fb_username_or_userid,
            new_reactions=new_reactions,
        )
        return {
            "fb_username_or_userid": fb_username_or_userid,
            "profile": profile_feed,
            "data": final_res,
            "raw_data": self.requests_parser.res_new,
        }
