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

# Support Me

If you enjoy this project and would like to support me, please consider donating 🙌  
Your support will help me continue developing this project and working on other exciting ideas!

## 💖 Ways to Support:

- **PayPal**: [https://www.paypal.me/faustren1z](https://www.paypal.me/faustren1z)
- **Buy Me a Coffee**: [https://buymeacoffee.com/faustren1z](https://buymeacoffee.com/faustren1z)

Thank you for your support!! 🎉

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
    days_limit = 100 # Number of days within which to scrape posts
    driver_path = "/Users/hongshangren/Downloads/chromedriver-mac-arm64_136/chromedriver" 
    fb_spider = fb_graphql_scraper(driver_path=driver_path, open_browser=False)
    res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_id, days_limit=days_limit,display_progress=True)
    # print(res)


## Example.2 - login in your facebook account to collect data
# if __name__ == "__main__":
    # facebook_user_name = "love.yuweishao"
    # facebook_user_id = "100044253168423"
    # fb_account = "facebook_account"
    # fb_pwd = "facebook_paswword"
    # days_limit = 30 # Number of days within which to scrape posts
    # driver_path = "/Users/hongshangren/Downloads/chromedriver-mac-arm64_136/chromedriver" 
    # fb_spider = fb_graphql_scraper(fb_account=fb_account,fb_pwd=fb_pwd, driver_path=driver_path, open_browser=False)
    # res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)
    # print(res)
    


```

### Optional parameters

- **display_progress**:  
  A boolean value (`True` or `False`).  
  If set to `True`, the scraper will display how many days of posts remain to be collected based on your `days_limit`.  
  For example, if `days_limit=180`, it will scrape posts from today back to 180 days ago.  
  During the process, the remaining days will be printed and decrease gradually until reaching 0 or below, at which point scraping stops.  
  Example output:  
  `439 more days of posts to collect.`

- **open_browser**:  
  If set to `True`, the scraper will launch a browser window.  
  This allows login-based scraping (if `fb_account` and `fb_pwd` are provided), which may access more content.  
  However, this mode consumes more memory and **does not guarantee that your Facebook account will avoid being blocked**.  
  It is also useful for debugging if scraping fails or unexpected behavior occurs.

- **fb_username_or_userid**:  
  The Facebook Group ID, Fan Page ID, User ID, or User Name to scrape posts from.

- **days_limit**:  
  The number of days of posts to retrieve, counting backwards from today.

- **fb_account**:  
  Your Facebook account (Login-based scraping is still under maintenance.)

- **fb_pwd**:  
  Your Facebook account password (Login-based scraping is still under maintenance.)



## Result example

```python
{'fb_username_or_userid': '100044253168423',
 'profile': ['任何工作事宜請洽 高先生',
  '聯絡信箱：hawa00328@gmail.com',
  '聯絡電話：0975-386-266',
  'Page',
  ' · 演員',
  'hawa00328@gmail.com',
  'Not yet rated (0 Reviews)',
  '\ufeff',
  '1,484,829 followers'],
 'data': [{'post_id': '1245565493595211',
   'post_url': 'https://www.facebook.com/1245565493595211',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-05-09 09:14:42'),
   'published_date2': '2025-05-09',
   'time': 1746782082,
   'reaction_count.count': 3566,
   'comment_rendering_instance.comments.total_count': 55,
   'share_count.count': 13,
   'sub_reactions': {'讚': 3273, '大心': 283, '加油': 6, '哈': 2, '哇': 2},
   'context': '溫柔的大貓咪\n緬因貓～～～～～～\n好喜歡❤️❤️❤️',
   'video_view_count': None},
  {'post_id': '1243688160449611',
   'post_url': 'https://www.facebook.com/1243688160449611',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-05-06 12:38:46'),
   'published_date2': '2025-05-06',
   'time': 1746535126,
   'reaction_count.count': 3270,
   'comment_rendering_instance.comments.total_count': 59,
   'share_count.count': 22,
   'sub_reactions': {'讚': 2978, '大心': 282, '加油': 8, '哈': 2},
   'context': '💛',
   'video_view_count': None},
  {'post_id': '1242879413863819',
   'post_url': 'https://www.facebook.com/1242879413863819',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-05-05 10:02:32'),
   'published_date2': '2025-05-05',
   'time': 1746439352,
   'reaction_count.count': 3868,
   'comment_rendering_instance.comments.total_count': 55,
   'share_count.count': 28,
   'sub_reactions': {'讚': 3493, '大心': 362, '加油': 9, '哈': 3, '哇': 1},
   'context': '愛的表達方式有很多，\n真誠言語直接的愛、\n以行動表達溫度的愛，\n又或是充滿美麗魔法的愛！ \n\n母親節就給媽媽一份加滿心意以及滿滿美麗的禮物吧！\n#潤姬桃子 的愛的魔法\n祝媽媽母親節快樂💗\n\n@uruhime.momoko.official',
   'video_view_count': None},
  {'post_id': '1239140660904361',
   'post_url': 'https://www.facebook.com/1239140660904361',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-04-30 09:01:18'),
   'published_date2': '2025-04-30',
   'time': 1746003678,
   'reaction_count.count': 3455,
   'comment_rendering_instance.comments.total_count': 42,
   'share_count.count': 12,
   'sub_reactions': {'讚': 3249, '大心': 199, '哈': 4, '加油': 2, '哇': 1},
   'context': '紐約碎片。\n\n沒注意到主人在，\n拍完往後轉抖了一大下。\n點點頭🙂\u200d↕️對了主人比個大拇指（意義不明？）',
   'video_view_count': None},
  {'post_id': '1237090651109362',
   'post_url': 'https://www.facebook.com/1237090651109362',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-04-27 12:56:19'),
   'published_date2': '2025-04-27',
   'time': 1745758579,
   'reaction_count.count': 4682,
   'comment_rendering_instance.comments.total_count': 25,
   'share_count.count': 12,
   'sub_reactions': {'讚': 4354, '大心': 311, '加油': 11, '哈': 5, '哇': 1},
   'context': '回家抱老迪 （請自動忽略阿爸）\n迪底撿回來也11年了，希望你也健康幸福。\n希望家人們都平安健康快樂。\n\n#迪底是阿筆的第一個兄弟',
   'video_view_count': None},
  {'post_id': '1236471601171267',
   'post_url': 'https://www.facebook.com/1236471601171267',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-04-26 16:23:29'),
   'published_date2': '2025-04-26',
   'time': 1745684609,
   'reaction_count.count': 3004,
   'comment_rendering_instance.comments.total_count': 41,
   'share_count.count': 13,
   'sub_reactions': {'讚': 2789, '大心': 210, '哈': 3, '加油': 2},
   'context': '剛在坐高鐵時，覺得時間實在是過得太快了。\n還來不及消化感受些什麼，轉頭又得先離開。\n一天當三天用確實感覺很精彩，\n但是不是錯過太多細節了呢？ 晚安',
   'video_view_count': None},
  {'post_id': '1235381784613582',
   'post_url': 'https://www.facebook.com/1235381784613582',
   'username_or_userid': '100044253168423',
   'owing_profile': {'__typename': 'User',
    'name': '邵雨薇',
    'short_name': '邵雨薇',
    'id': '100044253168423'},
   'published_date': Timestamp('2025-04-25 05:49:56'),
   'published_date2': '2025-04-25',
   'time': 1745560196,
   'reaction_count.count': 6846,
   'comment_rendering_instance.comments.total_count': 101,
   'share_count.count': 40,
   'sub_reactions': {'讚': 6405, '大心': 408, '加油': 19, '哈': 14},
   'context': '偶爾需要遇見一道彩虹，\n雨後剛轉天晴時，就像一個新希望。',
   'video_view_count': None}
 ]
}
```

### Notes
- If you choose to collect data by logging into your account, you may face the risk of your account being blocked, even if this program only scrolls through Facebook web pages.
- Reaction Categories (EN): [`like`, `haha`, `angry`, `love`, `care`, `wow`, `sad`]
- Reaction Categories (TW): [`讚`, `哈`, `怒`, `大心`, `加油`, `哇`, `嗚`]


```python

## To-Do

- Login-based scraping