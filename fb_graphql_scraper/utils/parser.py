# -*- coding: utf-8 -*-
import pandas as pd
from seleniumwire.utils import decode
import json
from fb_graphql_scraper.utils.utils import *


class RequestsParser(object):
    def __init__(self, driver) -> None:
        self.driver = driver
        self.res_new = []
        self.feedback_list = []
        self.context_list = []
        self.creation_list = []
        self.author_id_list = []
        self.author_id_list2 = []
        self.reaction_names = ["讚", "哈", "怒", "大心", "加油", "哇", "嗚"]
        self.en_reaction_names = ["like", "haha", "angry", "love", "care", "sorry", "wow"]

    def get_graphql_body_content(self, req_response, req_url):
        target_url = "https://www.facebook.com/api/graphql/"
        if req_response and req_url == target_url:
            response = req_response
            body = decode(response.body, response.headers.get(
                'Content-Encoding', 'identity'))
            body_content = body.decode("utf-8").split("\n")
            return body_content
        return None

    def parse_body(self, body_content):
        for each_body in body_content:
            json_data = json.loads(each_body)
            self.res_new.append(json_data)
            try:
                each_res = json_data['data']['node'].copy()
                each_feedback = find_feedback_with_subscription_target_id(
                    each_res)
                if each_feedback:
                    self.feedback_list.append(each_feedback)
                    message_text = find_message_text(json_data)
                    creation_time = find_creation(json_data)
                    if message_text:
                        self.context_list.append(message_text)
                    elif not message_text:
                        self.context_list.append(None)
                    if creation_time:
                        self.creation_list.append(creation_time)

            # Did not display or record error message at here
            except Exception as e:
                pass

    def collect_posts(self):
        res_out = []
        for each in self.feedback_list:
            res_out.append({
                "post_id": each['subscription_target_id'],
                "reaction_count": each['reaction_count'],
                "top_reactions": each['top_reactions'],
                "share_count": each['share_count'],
                "comment_rendering_instance": each['comment_rendering_instance'],
                "video_view_count": each['video_view_count']
            })
        return res_out

    def convert_res_to_df(self, res_in):
        df_res = pd.json_normalize(res_in)
        df_res = df_res[[
            'post_id',
            'reaction_count.count',
            'comment_rendering_instance.comments.total_count',
            'share_count.count',
            'top_reactions.edges',
            'video_view_count'
        ]]
        return df_res

    def process_reactions(self, reactions_in):
        reaction_names = self.reaction_names
        en_reaction_names = self.en_reaction_names # if you are in U.S, use self.en_reaction_names
        reaction_hash = {}
        for each_react in reactions_in:
            reaction_hash[each_react['node']['localized_name']
                          ] = each_react['reaction_count']  # get reaction value

        # for k in reaction_names:
        #     if k not in reaction_hash and k not in en_reaction_names:
        #         reaction_hash[k] = '0'
        return reaction_hash
