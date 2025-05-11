# -*- coding: utf-8 -*-
import concurrent.futures as futures
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import time
import json


# if key: 'subscription_target_id' in feedback, store this feedback
def find_feedback_with_subscription_target_id(data):
    if isinstance(data, dict):
        if 'feedback' in data and isinstance(data['feedback'], dict):
            feedback = data['feedback']
            if 'subscription_target_id' in list(feedback.keys()):
                return feedback

        # Traverse the values of the dictionary and continue recursively searching
        for value in data.values():
            result = find_feedback_with_subscription_target_id(value)
            if result:
                return result

    # If it is a list, traverse each element in the list and continue recursively searching
    elif isinstance(data, list):
        for item in data:
            result = find_feedback_with_subscription_target_id(item)
            if result:
                return result

    # If no matching feedback is found, return None
    return None


def find_message_text(data):
    if isinstance(data, dict):
        # type is dict，check 'story' key
        if 'story' in data:
            # if key 'story's value type is dict, and include 'message' key
            if isinstance(data['story'], dict) and 'message' in data['story']:
                # if key 'message's value type is dict, and include 'text' key
                if isinstance(data['story']['message'], dict) and 'text' in data['story']['message']:
                    # return 'text' key
                    return data['story']['message']['text']

        # recursively check each value in dict if can not find anything
        for value in data.values():
            result = find_message_text(value)
            if result:
                return result
    elif isinstance(data, list):
        # if array, check each element recursively
        for item in data:
            result = find_message_text(item)
            if result:
                return result
    # 如果沒有符合條件的值，return None
    return None


def find_creation(data):
    if isinstance(data, dict):
        # If it's a dictionary, check if it contains the 'story' key
        if 'story' in data:
            # If the value of the 'story' key is a dictionary and contains the 'creation_time' key
            if isinstance(data['story'], dict) and 'creation_time' in data['story']:
                # Return the value of the 'creation_time' key
                return data['story']['creation_time']

        # If no matching condition is found, recursively check each value in the dictionary
        for value in data.values():
            result = find_creation(value)
            if result:
                return result

    elif isinstance(data, list):
        # If it's a list, recursively check each element in the list
        for item in data:
            result = find_creation(item)
            if result:
                return result
    # If no matching condition is found, return None
    return None


def find_actors(data):
    if isinstance(data, dict):
        # If it's a dictionary, check if it contains the 'story' key
        if 'story' in data:
            # If the value of the 'story' key is a dictionary and contains the 'actors' key
            if isinstance(data['story'], dict) and 'actors' in data['story']:
                # Return the value of the 'id' key under 'actors'
                return data['story']['actors']['id']

        # If no matching condition is found, recursively check each value in the dictionary
        for value in data.values():
            result = find_actors(value)
            if result:
                return result

    elif isinstance(data, list):
        # If it's a list, recursively check each element in the list
        for item in data:
            result = find_actors(item)
            if result:
                return result
    # If no matching condition is found, return None
    return None


def find_owning_profile(data):
    if isinstance(data, dict):
        # If it's a dictionary, check if it contains the 'story' key
        if 'owning_profile' in data:
            # If the value of the 'story' key is a dictionary and contains the 'actors' key
            if isinstance(data['owning_profile'], dict):
                # Return the value of the 'id' key under 'actors'
                return data['owning_profile']

        # If no matching condition is found, recursively check each value in the dictionary
        for value in data.values():
            result = find_owning_profile(value)
            if result:
                return result

    elif isinstance(data, list):
        # If it's a list, recursively check each element in the list
        for item in data:
            result = find_owning_profile(item)
            if result:
                return result
    # If no matching condition is found, return None
    return None


def timeout(timelimit):
    def decorator(func):
        def decorated(*args, **kwargs):
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    print('Time out!')
                    raise TimeoutError from None
                else:
                    pass
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result
        return decorated
    return decorator


def get_current_time(timezone="Asia/Taipei"):
    current_time_utc = datetime.utcnow()
    target_timezone = pytz.timezone(timezone)
    target_current_time = current_time_utc.replace(
        tzinfo=pytz.utc).astimezone(target_timezone)
    return target_current_time


def days_difference_from_now(tmp_creation_array: list) -> int:
    """計算第一次發文日期與當前日間隔天數

    Args:
        tmp_creation_array (list): _description_

    Returns:
        int: 間隔天數
    """
    timestamp = min(tmp_creation_array)
    current_date_time = datetime.now()
    date_time_obj = datetime.fromtimestamp(timestamp)
    difference = current_date_time - date_time_obj
    return difference.days


def is_date_exceed_limit(max_days_ago, days_limit: int = 61):
    if max_days_ago > days_limit:
        return True
    return False

def pause(pause_time: int = 1):
    time.sleep(pause_time)


def get_payload(doc_id_in: str, id_in: str, before_time: str = None):
    variables_dict = {
        "afterTime": None,
        "beforeTime": before_time,
        "count": 3,
        "cursor": None,
        "feedLocation": "TIMELINE",
        "feedbackSource": 0,
        "focusCommentID": None,
        "memorializedSplitTimeFilter": None,
        "omitPinnedPost": True,
        "postedBy": {"group": "OWNER"},
        "privacy": {"exclusivity": "INCLUSIVE", "filter": "ALL"},
        "privacySelectorRenderLocation": "COMET_STREAM",
        "renderLocation": "timeline",
        "scale": 3,
        "stream_count": 1,
        "taggedInOnly": False,
        "useDefaultActor": False,
        "id": id_in,
        "__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider": False,
        "__relay_internal__pv__IsWorkUserrelayprovider": False,
        "__relay_internal__pv__IsMergQAPollsrelayprovider": False,
        "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False,
        "__relay_internal__pv__CometUFIShareActionMigrationrelayprovider": False,
        "__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider": False,
        "__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider": False,
        "__relay_internal__pv__StoriesRingrelayprovider": False,
        "__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider": False
    }

    payload_out = {
        "variables": json.dumps(variables_dict),
        "doc_id": doc_id_in
    }
    return payload_out

def get_next_payload(
    doc_id_in:str, 
    id_in:str, 
    before_time:str, 
    cursor_in:str
):
    variables_dict = {
        "afterTime": None,
        "beforeTime": before_time,
        "count": 3,
        "cursor": cursor_in,
        "feedLocation": "TIMELINE",
        "feedbackSource": 0,
        "focusCommentID": None,
        "memorializedSplitTimeFilter": None,
        "omitPinnedPost": True,
        "postedBy": {"group": "OWNER"},
        "privacy": {"exclusivity": "INCLUSIVE", "filter": "ALL"},
        "privacySelectorRenderLocation": "COMET_STREAM",
        "renderLocation": "timeline",
        "scale": 3,
        "stream_count": 1,
        "taggedInOnly": False,
        "useDefaultActor": False,
        "id": id_in,
        "__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider": False,
        "__relay_internal__pv__IsWorkUserrelayprovider": False,
        "__relay_internal__pv__IsMergQAPollsrelayprovider": False,
        "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False,
        "__relay_internal__pv__CometUFIShareActionMigrationrelayprovider": False,
        "__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider": False,
        "__relay_internal__pv__StoriesTrayShouldShowMetadatarelayprovider": False,
        "__relay_internal__pv__StoriesRingrelayprovider": False,
        "__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider": False
    }
    payload_out = {
        "variables": json.dumps(variables_dict),
        "doc_id": doc_id_in
    }
    return payload_out

def get_next_cursor(body_content_in):
    for i in range(len(body_content_in)-1, -1, -1):
        try:
            json_tail = json.loads(body_content_in[i])
            nex_cursor = json_tail.get("data").get(
                "page_info").get("end_cursor")
            return nex_cursor
        except AttributeError:
            pass

def get_next_page_status(body_content):
    for each_body in body_content:
        try:
            tmp_json = json.loads(each_body)
            next_page_status = tmp_json.get("data").get(
                "page_info").get("has_next_page")
            return next_page_status
        except Exception as e:
            pass
    return True # sometimes, scraper can not collect API's "has_next" info, Program choose return True, I will improve this step in the near future.


def compare_timestamp(timestamp: int, days_limit: int, display_progress: bool) -> bool:
    timestamp_date = datetime.utcfromtimestamp(timestamp).date()
    current_date = datetime.utcnow().date()
    past_date = current_date - timedelta(days=days_limit)
    if display_progress:
        days_remaining = (timestamp_date - past_date).days
        if days_remaining > 0:
            print(f"{days_remaining} more days of posts to collect.")
        else:
            print("Target days reached or exceeded.")
    return timestamp_date < past_date


def get_before_time(time_zone='Asia/Taipei'):
    location_tz = pytz.timezone(time_zone)
    current_time = datetime.now(location_tz)
    timestamp = str(int(current_time.timestamp()))
    return timestamp

def get_posts_image(post_id:str):
    url = f"https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Ftoolbox003%2Fposts%2F{post_id}&show_text=true&width=800"
    """You can check out the content through the link 
    to better understand what I'm talking about haha"""
    response = requests.get(url=url)
    response.status_code
    soup = BeautifulSoup(response.text, "html.parser")
    pattern = re.compile(r"^https://scontent")
    all_src_links = [tag['src'] for tag in soup.find_all(src=pattern)]
    return all_src_links