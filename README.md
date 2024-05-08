# Facebook GraphQL Scraper

## Install

To install the latest release from PyPI:

```sh
pip install facebook-graphql-scraper
```

## Requirements

```sh
ipython==8.19.0
pytz==2023.3.post1
selenium_wire==5.1.0
tqdm==4.66.1
```

### Usage

You can choose between two methods to collect user posts data. 
- **Pleas setup driver path at first**
- **Log in with your account credentials**: login facebook account
- **Without logging in**: Without logging in, click the X icon to 
- **Difference**: The difference between these two methods is that for some personal accounts, you cannot browse the user's posts without logging into a Facebook account.

```python
# -*- coding: utf-8 -*-
from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper


## Example.1 - without logging in
if __name__ == "__main__":
    facebook_user_name = "KaiCenatOfficial"
    facebook_user_id = "100087298771006"
    days_limit = 30 # Number of days within which to scrape posts
    driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
    fb_spider = fb_graphql_scraper(driver_path=driver_path)
    res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
    print(res)


## Example.2 - login in your facebook account to collect data
# if __name__ == "__main__":
    # facebook_user_name = "KaiCenatOfficial"
    # facebook_user_id = "100087298771006"
    # fb_account = "facebook_account"
    # fb_pwd = "facebook_paswword"
    # days_limit = 30 # Number of days within which to scrape posts
    # driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
    # fb_spider = fb_graphql_scraper(fb_account=fb_account,fb_pwd=fb_pwd,driver_path=driver_path)
    # res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
    # print(res)
    


```

### Optional parameters

- **fb_account**: your facebook account
- **fb_pwd**: your facebook account password
- **fb_username_or_userid**: groups, fan page, account User-ID or User-Name.
- **days_limit**: Number of days within which to scrape posts..


## Result example

```python
{'fb_username_or_userid': 'KaiCenatOfficial',
 'profile': ['Come Through & Watch These Litt CLIPS!',
             'Page',
             ' · Digital creator',
             'youtube.com/c/KaiCenat'],
 'data': [{'post_id': '406275965625693',
           'post_url': 'https://www.facebook.com/406275965625693',
           'username_or_userid': 'KaiCenatOfficial',
           'owing_profile': {'__typename': 'User',
                             'name': 'Kai Cenat',
                             'short_name': 'Kai Cenat',
                             'id': '100087298771006'},
           'published_date': Timestamp('2024-05-06 16:00:03'),
           'published_date2': '2024-05-06',
           'time': 1715011203,
           'reaction_count.count': 978,
           'comment_rendering_instance.comments.total_count': 62,
           'share_count.count': 17,
           'sub_reactions': {'Like': 678,
                             'Love': 181,
                             'Haha': 105,
                             'Care': 12,
                             'Wow': 2},
           'context': 'This Nigerian school was crazy 🤯',
           'video_view_count': 6599},
          {'post_id': '406274102292546',
           'post_url': 'https://www.facebook.com/406274102292546',
           'username_or_userid': 'KaiCenatOfficial',
           'owing_profile': {'__typename': 'User',
                             'name': 'Kai Cenat',
                             'short_name': 'Kai Cenat',
                             'id': '100087298771006'},
           'published_date': Timestamp('2024-05-05 16:00:04'),
           'published_date2': '2024-05-05',
           'time': 1714924804,
           'reaction_count.count': 1376,
           'comment_rendering_instance.comments.total_count': 32,
           'share_count.count': 33,
           'sub_reactions': {'Like': 857,
                             'Haha': 499,
                             'Love': 13,
                             'Sad': 4,
                             'Care': 2,
                             'Wow': 1},
           'context': 'The hardest challenge 😂',
           'video_view_count': 21064},
          {'post_id': '406270758959547',
           'post_url': 'https://www.facebook.com/406270758959547',
           'username_or_userid': 'KaiCenatOfficial',
           'owing_profile': {'__typename': 'User',
                             'name': 'Kai Cenat',
                             'short_name': 'Kai Cenat',
                             'id': '100087298771006'},
           'published_date': Timestamp('2024-05-04 16:00:05'),
           'published_date2': '2024-05-04',
           'time': 1714838405,
           'reaction_count.count': 9309,
           'comment_rendering_instance.comments.total_count': 97,
           'share_count.count': 111,
           'sub_reactions': {'Like': 5991,
                             'Haha': 2727,
                             'Love': 534,
                             'Care': 36,
                             'Wow': 12,
                             'Sad': 8,
                             'Angry': 1},
           'context': '24 hours with IShowSpeed 🚨',
           'video_view_count': 303210},
          {'post_id': '405533315699958',
           'post_url': 'https://www.facebook.com/405533315699958',
           'username_or_userid': 'KaiCenatOfficial',
           'owing_profile': {'__typename': 'User',
                             'name': 'Kai Cenat',
                             'short_name': 'Kai Cenat',
                             'id': '100087298771006'},
           'published_date': Timestamp('2024-05-03 16:00:14'),
           'published_date2': '2024-05-03',
           'time': 1714752014,
           'reaction_count.count': 1383,
           'comment_rendering_instance.comments.total_count': 39,
           'share_count.count': 24,
           'sub_reactions': {'Like': 823,
                             'Haha': 522,
                             'Love': 30,
                             'Wow': 4,
                             'Care': 3,
                             'Sad': 1},
           'context': "Speed's rizz needs some help 😱",
           'video_view_count': 387201}]
}
```

### Notes
- If you choose to collect data by logging into your account, you may face the risk of your account being blocked, even if this program only scrolls through Facebook web pages.
- Reaction Categories (EN): [`like`, `haha`, `angry`, `love`, `care`, `wow`, `sad`]
- Reaction Categories (TW): [`讚`, `哈`, `怒`, `大心`, `加油`, `哇`, `嗚`]


```python

## To-Do

- Collect profile info
- Collect image info