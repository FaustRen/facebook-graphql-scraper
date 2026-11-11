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
    days_limit = 20 # Number of days within which to scrape posts
    driver_path = "/Users/hongshangren/Downloads/chromedriver-mac-arm64_157/chromedriver" 
    fb_spider = fb_graphql_scraper(driver_path=driver_path, open_browser=False)
    res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_id, days_limit=days_limit,display_progress=True)
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

```json
{
  "fb_username_or_userid": "100044253168423",
  "profile": [
    "聯絡電話：0975-386-266",
    "Page",
    " · 演員",
    "hawa00328@gmail.com",
    "Not yet rated (3 reviews)",
    "\ufeff",
    "1,451,355 followers"
  ],
  "profile_picture": "https://scontent.ftpe7-3.fna.fbcdn.net/v/t39.30808-1/432384560_970902114394885_7123123077107726953_n.jpg?stp=dst-jpg_tt6&cstp=mx1080x1080&ctp=s720x720&_nc_cat=104&_nc_map=urlgen_bucketless&ccb=1-7&_nc_sid=3ab345&_nc_ohc=C9GPTPyK0hwQ7kNvwHTFdFF&_nc_oc=AdrWDzntYtzvcmUOpRnpswB1JYapb0E4Wwx9ZCDJfrvnEwFIt9V0sIPLt7Xt7TNyMMs&_nc_zt=24&_nc_ht=scontent.ftpe7-3.fna&_nc_gid=CCybvl4ONI1JyrxIM5N9dw&_nc_ss=7f289&oh=00_AQSHf0MMg2v1TJCMz52vEHkdrTiVTwQhPTlaJxO9G3UWPw&oe=6AFAA4A3",
  "data": [
    {
      "post_id": "1687825662702523",
      "post_url": "https://www.facebook.com/1687825662702523",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-11-03 13:05:37",
      "published_date2": "2026-11-03",
      "time": 1793711137,
      "reaction_count.count": 2203,
      "comment_rendering_instance.comments.total_count": 24,
      "share_count.count": 12,
      "sub_reactions": {
        "讚": 2008,
        "大心": 189,
        "哈": 3,
        "加油": 2,
        "哇": 1
      },
      "context": "日常是…\n被duolingo 情勒 繼續練習語言、\n滑好笑reels滑太晚、\n把自己拔出沙發去洗澡、\n早上起床與棉被對抗。\n\n生活想要有趣、生活需要規律\n3C重度使用者要吃葉黃素，\n保護心血管又抗發炎要吃魚油。\n\n🌼金盞花葉黃素軟膠囊Plus\n🐟 日本原裝進口85%高OMEGA3魚油\n\n即日起至11/13（五） 11:00\n趁雙11優惠一次把康萃魚油葉黃素補齊吧\nbeezintw\nhttps://yaoyao.biz/sdgHq",
      "video_view_count": null
    },
    {
      "post_id": "1686457486172674",
      "post_url": "https://www.facebook.com/1686457486172674",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-11-02 04:06:42",
      "published_date2": "2026-11-02",
      "time": 1793592402,
      "reaction_count.count": 776,
      "comment_rendering_instance.comments.total_count": 12,
      "share_count.count": 4,
      "sub_reactions": {
        "讚": 686,
        "大心": 86,
        "哇": 3,
        "加油": 1
      },
      "context": "小編：粉潤對策是保養的基礎工程\n啟動好氣色\n這次日本味王在雙11準備了粉潤對策特別優惠，快塞滿你的購物車吧\n28 天明亮勻淨計劃，把光還給自己，讓陰影優雅消散。\nhttps://www.momoshop.com.tw/product/15653474\n\n#日本味王 #粉潤對策 #momo雙11",
      "video_view_count": null
    },
    {
      "post_id": "1681788199972936",
      "post_url": "https://www.facebook.com/1681788199972936",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-10-28 12:36:07",
      "published_date2": "2026-10-28",
      "time": 1793190967,
      "reaction_count.count": 1784,
      "comment_rendering_instance.comments.total_count": 14,
      "share_count.count": 5,
      "sub_reactions": {
        "讚": 1649,
        "大心": 124,
        "加油": 4,
        "哈": 4,
        "哇": 2,
        "怒": 1
      },
      "context": "今天的狀態，粉潤剛剛好！\n日本味王「粉潤對策」\n新廣告登場✨\n\n#日本味王 #粉潤對策",
      "video_view_count": null
    },
    {
      "post_id": "1680624306755992",
      "post_url": "https://www.facebook.com/1680624306755992",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-10-27 09:12:27",
      "published_date2": "2026-10-27",
      "time": 1793092347,
      "reaction_count.count": 3647,
      "comment_rendering_instance.comments.total_count": 43,
      "share_count.count": 43,
      "sub_reactions": {
        "讚": 3346,
        "大心": 285,
        "加油": 9,
        "哈": 3,
        "哇": 3,
        "嗚": 1
      },
      "context": "謝謝金鐘61🤍\n好值得收藏在記憶裡的一天\n\n👗louisvuitton #LouisVuitton\n💎bvlgari",
      "video_view_count": null
    },
    {
      "post_id": "1673892820762474",
      "post_url": "https://www.facebook.com/1673892820762474",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-10-20 11:00:42",
      "published_date2": "2026-10-20",
      "time": 1792494042,
      "reaction_count.count": 1283,
      "comment_rendering_instance.comments.total_count": 26,
      "share_count.count": 13,
      "sub_reactions": {
        "讚": 1118,
        "大心": 154,
        "哈": 5,
        "加油": 3,
        "哇": 2,
        "嗚": 1
      },
      "context": "第二年擔任MIXX平台的代言人\n滿心期待每個將送來的包裹\n\nMIXX雙十一將帶給大家更多質感選物\n快來跟我一起下單吧\n\n#MIXX #MIXX質感美學選物平台 #MIXX雙十一",
      "video_view_count": null
    },
    {
      "post_id": "1670182317800191",
      "post_url": "https://www.facebook.com/1670182317800191",
      "username_or_userid": "100044253168423",
      "owing_profile": {
        "__typename": "User",
        "name": "邵雨薇",
        "short_name": "邵雨薇",
        "id": "100044253168423"
      },
      "published_date": "2026-10-16 12:52:53",
      "published_date2": "2026-10-16",
      "time": 1792155173,
      "reaction_count.count": 8298,
      "comment_rendering_instance.comments.total_count": 110,
      "share_count.count": 236,
      "sub_reactions": {
        "讚": 7591,
        "大心": 649,
        "加油": 30,
        "哇": 17,
        "哈": 10,
        "嗚": 1
      },
      "context": "穿搭沒有標準答案，喜歡就好。\n\n除了衣服本身，我在意的\n還有那些讓整體更好看的小細節。\n穿出自己喜歡的樣子，就是最好的風格。\n@曼黛瑪璉  #雙弧\n\nhttps://bmai.app/c13bd4b5\n\n#曼黛瑪璉 #迷人雙弧 #挺美",
      "video_view_count": null
    }
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