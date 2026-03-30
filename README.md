# fb_scraper_request

Scrape public Facebook posts without login using a simple, requests-based scraper.

This project is a streamlined fork developed from the foundational work at [FaustRen/facebook-graphql-scraper](https://github.com/FaustRen/facebook-graphql-scraper).

## Improvements
- **Lightweight:** Uses only `requests` to fetch user posts—no browser, Selenium, or Playwright required.
- **Focused:** Removed login-dependent features to focus exclusively on public page scraping.
- **Efficient:** Optimized for speed and minimal dependency overhead.

## Install

```bash
pip install fb_scraper_request
```

## Quick Example

```python
from fb_scraper_request import FacebookGraphqlScraper

# Initialize the scraper
fb = FacebookGraphqlScraper()

# Get posts from a specific username with a day limit
result = fb.get_user_posts("honghotduongpho.official00", days_limit=3)

for post in result["data"]:
    print(f"Content: {post['context']}")
    print(f"Likes: {post['reaction_count.count']}")
    print("-" * 20)
```

## Results
The result object returns a structured dictionary containing profile info and a list of post data:
```json
{
"fb_username_or_userid": "100063640556423",
    "profile": [
        "Life at VNG | Ho Chi Minh City"
    ],
    "data": [
        {
            "post_id": "1601334011997935",
            "post_url": "https://www.facebook.com/1601334011997935",
            "username_or_userid": "100063640556423",
            "owing_profile": {
                "__typename": "User",
                "name": "Life at VNG",
                "short_name": "Life at VNG",
                "id": "100063640556423"
            },
            "published_date": "2026-03-28T11:58:04",
            "published_date2": "2026-03-28",
            "time": 1774673884,
            "reaction_count.count": 16,
            "comment_rendering_instance.comments.total_count": null,
            "share_count.count": null,
            "sub_reactions": {
                "Thích": 10,
                "Yêu thích": 5,
                "Wow": 1
            },
            "context": "[HÀ NỘI] BUSINESS DEVELOPMENT FRESHER 2026 “BẬT ĐỊNH VỊ” HẸN GẶP SINH VIÊN THỦ ĐÔ 📍\n✨ Ứng tuyển Business Development Fresher 2026 tại: https://bit.ly/4rRnqaG \n\nBusiness Development Fresher 2026 (BDF 2026) - chương trình tuyển chọn và phát triển thế hệ Business Development tiềm năng của VNG ZingPlay Game Studios đã sẵn sàng gặp gỡ và giao lưu cùng các bạn sinh viên Hà Nội.\n\n👉 Nếu bạn đam mê khám phá thị trường Game,...",
            "video_view_count": null
        },
        ...
    ],
    "raw_data": [
        <raw_facebook_meta_response>
    ]
}
```

## Extracting Additional Data

> **Note:** If you need more data fields than what's provided in `data`, you can manually extract additional information from `raw_data`. This contains the complete raw Facebook GraphQL API responses.

```python
result = fb.get_user_posts("page_username", days_limit=3)

# Access raw API responses for custom data extraction
for raw_response in result["raw_data"]:
    # Extract any custom fields you need
    custom_field = raw_response.get("your_custom_field")
```

## Credits

Thank you to the original project owner [FaustRen](https://github.com/FaustRen) and the [facebook-graphql-scraper](https://github.com/FaustRen/facebook-graphql-scraper) repository for the foundational work that made this simplified version possible.
