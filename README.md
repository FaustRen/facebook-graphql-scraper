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
    facebook_user_name = "love.yuweishao"
    facebook_user_id = "100044253168423"
    days_limit = 30 # Number of days within which to scrape posts
    driver_path = "/Users/renren/Desktop/FB_graphql_scraper拷貝/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver" 
    fb_spider = fb_graphql_scraper(driver_path=driver_path)
    res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
    print(res)


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
    


```

### Optional parameters

- **fb_username_or_userid**: groups, fan page, account User-ID or User-Name.
- **timeout**: How many seconds to wait before timing out. Default is 600.
- **looptimes**: The program scrolls down Facebook pages..


## Result example

```python
{'fb_username_or_userid': 'love.yuweishao',
 'profile': ['任何工作事宜請洽 高先生',
  '聯絡信箱：hawa00328@gmail.com',
  '聯絡電話：0975-386-266',
  '粉絲專頁',
  ' · 演員',
  'hawa00328@gmail.com',
  '1,497,248 位追蹤者'],
 'data': [{'post_id': '993720562113040',
   'post_url': 'https://www.facebook.com/993720562113040',
   'username_or_userid': 'love.yuweishao',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2024-04-24 17:42:14'),
   'published_date2': '2024-04-24',
   'time': 1713980534,
   'reaction_count.count': 3884,
   'comment_rendering_instance.comments.total_count': 34,
   'share_count.count': 10,
   'sub_reactions': {'讚': 3652, '大心': 226, '加油': 5, '哈': 1},
   'context': 'breathe and life',
   'video_view_count': nan},
  {'post_id': '993371658814597',
   'post_url': 'https://www.facebook.com/993371658814597',
   'username_or_userid': 'love.yuweishao',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2024-04-24 03:55:34'),
   'published_date2': '2024-04-24',
   'time': 1713930934,
   'reaction_count.count': 5043,
   'comment_rendering_instance.comments.total_count': 41,
   'share_count.count': 29,
   'sub_reactions': {'讚': 4632, '大心': 397, '加油': 8, '哇': 4, '哈': 2},
   'context': '夏季的雨天總讓人難以預期\n每日帶不帶傘的莫非定律 \n空間裡的黏膩和潮濕點滴\n通通都被D-26匯集在一起\n陰晴不定的天氣就交給最懂你的HYD❤️\n\nhttps://reurl.cc/Gjd9nv\nHYD 品宅趣\n#HYD #雙效清淨 #輕量設計 #除濕機',
   'video_view_count': nan},
  {'post_id': '992770662208030',
   'post_url': 'https://www.facebook.com/992770662208030',
   'username_or_userid': 'love.yuweishao',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2024-04-23 04:33:52'),
   'published_date2': '2024-04-23',
   'time': 1713846832,
   'reaction_count.count': 3286,
   'comment_rendering_instance.comments.total_count': 32,
   'share_count.count': 5,
   'sub_reactions': {'讚': 3150, '大心': 61, '加油': 59, '嗚': 13, '哇': 2, '哈': 1},
   'context': None,
   'video_view_count': nan},
  {'post_id': '992336592251437',
   'post_url': 'https://www.facebook.com/992336592251437',
   'username_or_userid': 'love.yuweishao',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2024-04-22 09:57:32'),
   'published_date2': '2024-04-22',
   'time': 1713779852,
   'reaction_count.count': 11892,
   'comment_rendering_instance.comments.total_count': 102,
   'share_count.count': 31,
   'sub_reactions': {'讚': 11164, '大心': 701, '加油': 15, '哈': 6, '哇': 5, '嗚': 1},
   'context': '母が撮った写真はとてもきれいです.🌸',
   'video_view_count': nan},
  {'post_id': '991854065633023',
   'post_url': 'https://www.facebook.com/991854065633023',
   'username_or_userid': 'love.yuweishao',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2024-04-21 12:34:39'),
   'published_date2': '2024-04-21',
   'time': 1713702879,
   'reaction_count.count': 5250,
   'comment_rendering_instance.comments.total_count': 43,
   'share_count.count': 13,
   'sub_reactions': {'讚': 4873, '大心': 364, '加油': 6, '哈': 4, '哇': 3},
   'context': '愛生活也愛工作🖤\n\n@michaelkors \n#MichaelKors',
   'video_view_count': nan}]
}
```

### Notes
- If you choose to collect data by logging into your account, you may face the risk of your account being blocked, even if this program only scrolls through Facebook web pages.
- Reaction Categories (EN): [`like`, `love`, `haha`, `sorry`, `wow`, `angry`, `care`]
- Reaction Categories (TW): [`讚`, `哈`, `怒`, `大心`, `加油`, `哇`, `嗚`]


```python

## To-Do

- Collect profile info
- Collect image info