from fb_scraper_request import FacebookGraphqlScraper
import json

fb = FacebookGraphqlScraper()
result = fb.get_user_posts("LifeAtVNG", days_limit=3)

for post in result["data"]:
    print(post["context"])
    print(f"Likes: {post['reaction_count.count']}")

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
