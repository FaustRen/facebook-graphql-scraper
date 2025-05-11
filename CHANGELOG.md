# Changelog

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/) and follows the [Keep a Changelog](https://keepachangelog.com/) format.

---

## [1.1.2] - 2025-05-11

### Added
- Introduced `open_browser` parameter in the `FacebookGraphqlScraper` initializer:  
  Allows opening the browser for manual Facebook login and easier debugging
- Added `get_posts_image(post_id)` utility function:  
  Retrieves embedded post images by parsing the post preview page

### Changed
- Refactored `get_user_posts` function:
  - Restored `display_progress` parameter to improve visibility of scraping progress
  - Mitigated issues with `days_limit` causing restarts from the beginning, improving efficiency
- Redesigned `requests_flow`:  
  Switched from using only `before_time` to an alternative fallback method to bypass Facebook's enhanced anti-scraping mechanism
- Modified `base_page.py`:  
  Enabled browser mode toggling based on `open_browser` flag

### Fixed
- Fixed premature termination logic in `get_user_posts` that caused incomplete post collection
- Improved debugging experience by providing clearer runtime outputs

---

## [1.1.1] - Previous Version

### Added
- Initial working version of `get_user_posts` function
- Basic GraphQL request flow for Facebook post scraping
