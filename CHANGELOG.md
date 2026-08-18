# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/) and follows the [Keep a Changelog](https://keepachangelog.com/) format.

---

## [1.1.7] - 2026-08-18

### Fixed

* Fixed anonymous Facebook timeline scraping failures caused by a newly required GraphQL Relay variable in `ProfileCometTimelineFeedRefetchQuery`
* Added `__relay_internal__pv__StoriesShouldEnablePhotosensitiveContentWarningrelayprovider` to `get_payload()` and `get_next_payload()` to match Facebook's currently required timeline GraphQL request structure
* Restored post parsing and pagination after GraphQL requests began returning:

  `missing_required_variable_value`

* Prevented the upstream GraphQL request failure from resulting in empty parser output and eventually surfacing as:

  `KeyError: 'post_id'`

### Notes

* This release is a compatibility hotfix for a change in Facebook's internal timeline GraphQL query
* Only the newly required Relay variable was added; other observed GraphQL runtime value differences were intentionally left unchanged because they are not currently required for successful scraping
* Facebook's GraphQL request structure is not a public stable API and may change again in future releases

---

## [1.1.6] - 2026-08-07

### Changed

* Updated the anonymous Facebook scraping bootstrap flow to improve compatibility with recent Facebook page behavior
* Removed redundant profile navigation that could reset captured network traffic and interfere with initial GraphQL request detection
* Simplified login popup dismissal to reduce timing issues before triggering timeline GraphQL requests
* Updated `get_payload()` and `get_next_payload()` to better match the currently observed Facebook timeline GraphQL request structure
* Added support for reusing the initial GraphQL cursor when sending the first replay request
* Improved pagination handling when `creation_time` cannot be parsed from a GraphQL response
* Improved output normalization when parser-generated fields contain incomplete or mismatched data

### Fixed

* Fixed anonymous scraping failures where the initial GraphQL payload could not be captured and the scraper eventually raised:

  `RuntimeError: Failed to extract initial graphql payload`

* Fixed failures caused by GraphQL responses no longer containing the expected post structure, which could eventually surface as:

  `KeyError: 'post_id'`

* Fixed progress checks that could fail when no post timestamps were parsed

* Reduced the likelihood of repeated Facebook login popup states preventing the scraper from reaching the GraphQL bootstrap stage

### Notes

* This release primarily restores compatibility with Facebook's currently observed anonymous timeline GraphQL flow
* The GraphQL request structure used by Facebook is not a public stable API and may change again in future releases

---

## [1.1.5] - 2026-05-11

### Fixed

* Rewrote `get_init_payload()` to safely skip captured requests that have no body or are missing `variables` / `doc_id`, returning `None` on failure instead of raising `UnboundLocalError`
* Raised a clear, actionable `RuntimeError` when the initial GraphQL payload can never be found, making bootstrap failures easier to diagnose

### Changed

* Improved headless mode stability in `base_page.py`:

  * Only maximize the window in `open_browser` mode; set a fixed `1920x1080` window size for headless runs via `--window-size`
  * Disabled automation-detection flags (`excludeSwitches`, `useAutomationExtension`) to reduce detection in headless mode
* Retried login popup dismissal up to 3 times to handle popups that can appear multiple times in headless mode, and extended page scrolling to more reliably trigger the timeline GraphQL request
* Trimmed the noisy Selenium stacktrace from the reject-button failure log message in `page_optional.py`

---

## [1.1.4] - 2025-11-26

### Fixed

* Repaired `click_reject_login_button()`, which had stopped working and caused the scraper to halt post collection
* Updated the `PageLocators.CLOSELOGIN` close-button XPath in `locator.py` (full-path replacement) to match Facebook's current login popup

---

## [1.1.3] - 2025-11-22

### Fixed

* Corrected an element locator issue in `facebook_graphql_scraper.py` that prevented proper retrieval of Facebook profile information (temporary patched release)

---

## [1.1.2] - 2025-05-11

### Added

* Introduced `open_browser` parameter in the `FacebookGraphqlScraper` initializer:

  * Allows opening the browser for manual Facebook login and easier debugging
* Added `get_posts_image(post_id)` utility function:

  * Retrieves embedded post images by parsing the post preview page

### Changed

* Refactored `get_user_posts()`:

  * Restored `display_progress` parameter to improve visibility of scraping progress
  * Mitigated issues with `days_limit` causing restarts from the beginning, improving efficiency
* Redesigned `requests_flow()`:

  * Switched from using only `before_time` to an alternative fallback method to improve compatibility with Facebook's anti-scraping behavior
* Modified `base_page.py`:

  * Enabled browser mode toggling based on the `open_browser` flag

### Fixed

* Fixed premature termination logic in `get_user_posts()` that caused incomplete post collection
* Improved debugging experience by providing clearer runtime outputs

---

## [1.1.1] - Previous Version

### Added

* Initial working version of `get_user_posts()`
* Basic GraphQL request flow for Facebook post scraping
