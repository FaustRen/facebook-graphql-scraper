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

- **Log in with your account credentials**: login facebook account
- **Without logging in**: Without logging in, click the X icon to 
- **Difference**: The difference between these two methods is that for some personal accounts, you cannot browse the user's posts without logging into a Facebook account.

```python
# -*- coding: utf-8 -*-
import os
from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from dotenv import load_dotenv


# ## Load account info
# load_dotenv()
fb_account = os.getenv("FBACCOUNT") # Facebook帳號密碼
pwd = os.getenv("FBPASSWORD")

# ## Log in account version
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
```

```python
# -*- coding: utf-8 -*-
import os
from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from dotenv import load_dotenv

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
```
### Optional parameters

- **fb_user_id**: group id/fans page id/account id.
- **timeout**: How many seconds to wait before timing out. Default is 600.
- **looptimes**: The program scrolls down Facebook pages..


## Post example

```python
[{'post_id': '385393337713956',
  'post_url': 'https://www.facebook.com/385393337713956',
  'username_or_userid': 'KaiCenatOfficial',
  'published_date': Timestamp('2024-03-31 16:00:39'),
  'published_date2': '2024-03-31',
  'time': 1711900839,
  'reaction_count.count': 1224,
  'comment_rendering_instance.comments.total_count': 37,
  'share_count.count': 32,
  'sub_reactions': {'讚': 802,
   '哈': 406,
   '大心': 9,
   '怒': 3,
   '加油': 2,
   '哇': 2,
   '嗚': '0'},
  'context': 'Druski Plays "What\'s In The Box?" 😱',
  'video_view_count': 15870},
 {'post_id': '387206327532657',
  'post_url': 'https://www.facebook.com/387206327532657',
  'username_or_userid': 'KaiCenatOfficial',
  'published_date': Timestamp('2024-03-30 12:01:06'),
  'published_date2': '2024-03-30',
  'time': 1711800066,
  'reaction_count.count': 7153,
  'comment_rendering_instance.comments.total_count': 154,
  'share_count.count': 67,
  'sub_reactions': {'讚': 5674,
   '哈': 1307,
   '大心': 121,
   '嗚': 22,
   '加油': 21,
   '哇': 8,
   '怒': '0'},
  'context': 'Kai Cenat Asks Tyla Out On A Date 😍 #viralreelsfb #comedy #kaicenat #reelsfb',
  'video_view_count': 73898},
 {'post_id': '385387707714519',
  'post_url': 'https://www.facebook.com/385387707714519',
  'username_or_userid': 'KaiCenatOfficial',
  'published_date': Timestamp('2024-03-29 17:01:39'),
  'published_date2': '2024-03-29',
  'time': 1711731699,
  'reaction_count.count': 1000,
  'comment_rendering_instance.comments.total_count': 47,
  'share_count.count': 15,
  'sub_reactions': {'讚': 762,
   '哈': 194,
   '大心': 34,
   '哇': 7,
   '加油': 2,
   '嗚': 1,
   '怒': '0'},
  'context': 'Chunkz Gets Hypnotised 😱',
  'video_view_count': 13763},
 {'post_id': '384078261178797',
  'post_url': 'https://www.facebook.com/384078261178797',
  'username_or_userid': 'KaiCenatOfficial',
  'published_date': Timestamp('2024-03-28 17:00:21'),
  'published_date2': '2024-03-28',
  'time': 1711645221,
  'reaction_count.count': 2587,
  'comment_rendering_instance.comments.total_count': 77,
  'share_count.count': 45,
  'sub_reactions': {'讚': 1905,
   '哈': 477,
   '大心': 186,
   '加油': 15,
   '哇': 4,
   '怒': '0',
   '嗚': '0'},
  'context': 'Trying The New Ice Spice Drink 😳',
  'video_view_count': 125605}
]
```

### Notes
- If you choose to collect data by logging into your account, you may face the risk of your account being blocked, even if this program only scrolls through Facebook web pages.
- Reaction Categories (EN): [`like`, `love`, `haha`, `sorry`, `wow`, `angry`, `care`]
- Reaction Categories (TW): [`讚`, `哈`, `怒`, `大心`, `加油`, `哇`, `嗚`]


```python

## To-Do

- Collect profile info
- Collect image info