# -*- coding: utf-8 -*-
import json
from urllib.parse import parse_qs, unquote
from fb_scraper_request.utils.utils import *


class RequestsParser(object):
    def __init__(self) -> None:
        # self.driver = driver
        self.reaction_names = ["讚", "哈", "怒", "大心", "加油", "哇", "嗚"]
        self.en_reaction_names = [
            "like",
            "haha",
            "angry",
            "love",
            "care",
            "sorry",
            "wow",
        ]

    def get_graphql_body_content(self, req_response, req_url):
        target_url = "https://www.facebook.com/api/graphql/"
        if req_response and req_url == target_url:
            response = req_response
            body = decode(
                response.body, response.headers.get("Content-Encoding", "identity")
            )
            body_content = body.decode("utf-8").split("\n")
            return body_content
        return None

    def _clean_res(self):
        self.res_new = []
        self.feedback_list = []
        self.context_list = []
        self.creation_list = []
        self.author_id_list = []
        self.author_id_list2 = []
        self.owning_profile = []

    def parse_body(self, body_content):
        for each_body in body_content:
            json_data = json.loads(each_body)
            self.res_new.append(json_data)
            try:
                each_res = json_data["data"]["node"].copy()
                each_feedback = find_feedback_with_subscription_target_id(each_res)
                if each_feedback:
                    self.feedback_list.append(each_feedback)
                    message_text = find_message_text(json_data)
                    creation_time = find_creation(json_data)
                    owing_profile = find_owning_profile(json_data)
                    if message_text:
                        self.context_list.append(message_text)
                    elif not message_text:
                        self.context_list.append(None)
                    if creation_time:
                        self.creation_list.append(creation_time)
                    self.owning_profile.append(owing_profile)

            # Did not display or record error message at here
            except Exception as e:
                pass

    def collect_posts(self):
        res_out = []
        for each in self.feedback_list:
            res_out.append(
                {
                    "post_id": each["subscription_target_id"],
                    "reaction_count": each["reaction_count"],
                    "top_reactions": each["top_reactions"],
                    "share_count": each["share_count"],
                    "comment_rendering_instance": each["comment_rendering_instance"],
                    "video_view_count": each["video_view_count"],
                }
            )
        return res_out

    def convert_res_to_df(self, res_in):
        # Pure Python version without pandas
        selected_fields = [
            "post_id",
            "reaction_count",
            "comment_rendering_instance",
            "share_count",
            "top_reactions",
            "video_view_count",
        ]
        result = []
        for item in res_in:
            row = {field: item.get(field) for field in selected_fields}
            result.append(row)
        return result

    def process_reactions(self, reactions_in) -> dict:
        """Extract sub reaction value:
        Args:
            reactions_in (_type_): _description_
        Returns:
            _dict_: {
                "like": value,
                "haha": value,
                "angry": value,
                "love": value,
                "care": value,
                "sorry": value,
                "wow": value
        }
        Note:
        """
        reaction_hash = {}
        for each_react in reactions_in:
            reaction_hash[each_react["node"]["localized_name"]] = each_react[
                "reaction_count"
            ]  # get reaction value
        return reaction_hash

    def extract_first_payload(self, payload: str):
        parsed_data = parse_qs(payload)
        print("Parsed data:", parsed_data)  # Debug: Show the parsed data
        decoded_data = {
            unquote(k): [unquote(v) for v in vals] for k, vals in parsed_data.items()
        }  # 解碼 keys 和 values
        first_payload = {
            k: v[0] for k, v in decoded_data.items()
        }  # 如果只需要第一個值作為字典中的單一值
        payload_variables = json.loads(first_payload["variables"])
        first_payload["variables"] = payload_variables
        print(first_payload)
        return first_payload
