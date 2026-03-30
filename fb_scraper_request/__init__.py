"""Facebook Scraper Request - Simple API to scrape public Facebook posts without login.

Example:
    from fb_scraper_request import FacebookGraphqlScraper

    fb = FacebookGraphqlScraper()
    result = fb.get_user_posts("vietgiaitri", days_limit=3)
    print(result["data"])
"""

from .facebook_graphql_scraper import FacebookGraphqlScraper

__version__ = "0.2.0"
__all__ = ["FacebookGraphqlScraper"]
