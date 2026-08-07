# -*- coding: utf-8 -*-
"""
Tests for FacebookGraphqlScraper.

Since the scraper requires Selenium / a live browser, all WebDriver
interactions are replaced with unittest.mock objects so the tests run
without any real browser or network traffic.
"""
import json
import os
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from urllib.parse import urlencode

# ── Helpers ──────────────────────────────────────────────────────────────────

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_graphql_response.json")


def _build_raw_request(variables: dict, doc_id: str = "9999", body_bytes: bytes = None):
    """Return a mock seleniumwire request object."""
    if body_bytes is None:
        payload = urlencode({"doc_id": doc_id, "variables": json.dumps(variables)})
        body_bytes = payload.encode("utf-8")
    req = MagicMock()
    req.url = "https://www.facebook.com/api/graphql/"
    req.body = body_bytes
    return req


def _make_scraper():
    """
    Build a FacebookGraphqlScraper instance with all Selenium dependencies
    mocked out so no browser is launched.
    """
    with patch("fb_graphql_scraper.facebook_graphql_scraper.BasePage") as MockBase, \
         patch("fb_graphql_scraper.facebook_graphql_scraper.PageOptional") as MockPage, \
         patch("fb_graphql_scraper.facebook_graphql_scraper.time") as mock_time:

        mock_time.sleep = MagicMock()

        scraper_cls = _import_scraper()
        scraper = scraper_cls.__new__(scraper_cls)

        # Set up minimal attributes the methods under test need
        scraper.fb_account = None
        scraper.fb_pwd = None
        scraper.driver_path = "/fake/chromedriver"
        scraper.pre_diff_days = float("-inf")
        scraper.counts_of_same_diff_days = 0
        scraper.post_id_list = []
        scraper.reaction_count_list = []
        scraper.profile_feed = []
        scraper.res = {
            "post_caption": [], "post_date": [], "post_likes": [],
            "comment_share_type": [], "comment_share_value": []
        }

        # Attach mock sub-objects
        scraper.base_page = MagicMock()
        scraper.page_optional = MagicMock()
        scraper.requests_parser = MagicMock()

        return scraper


def _import_scraper():
    from fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper
    return FacebookGraphqlScraper


# ── get_init_payload ──────────────────────────────────────────────────────────

class TestGetInitPayload:
    def test_returns_payload_with_valid_request(self):
        scraper = _make_scraper()
        variables = {"id": "123456", "count": 3}
        req = _build_raw_request(variables=variables, doc_id="7890")

        # extract_first_payload must return a real dict, not a mock
        from fb_graphql_scraper.utils.parser import RequestsParser
        real_parser = RequestsParser(driver=MagicMock())
        scraper.requests_parser = real_parser

        scraper.page_optional.driver.requests = [req]
        result = scraper.get_init_payload()

        assert result is not None
        assert result["doc_id"] == "7890"
        assert result["variables"]["id"] == "123456"

    def test_returns_none_when_no_graphql_requests(self):
        scraper = _make_scraper()
        non_graphql_req = MagicMock()
        non_graphql_req.url = "https://www.facebook.com/other/"
        non_graphql_req.body = b"irrelevant"
        scraper.page_optional.driver.requests = [non_graphql_req]

        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        result = scraper.get_init_payload()
        assert result is None

    def test_skips_requests_with_no_body(self):
        scraper = _make_scraper()
        req = MagicMock()
        req.url = "https://www.facebook.com/api/graphql/"
        req.body = None
        scraper.page_optional.driver.requests = [req]

        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        result = scraper.get_init_payload()
        assert result is None

    def test_skips_payload_missing_id_or_doc_id(self):
        """Payload without 'id' in variables should be skipped."""
        scraper = _make_scraper()
        # variables without 'id'
        req = _build_raw_request(variables={"count": 3}, doc_id="")
        scraper.page_optional.driver.requests = [req]

        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        result = scraper.get_init_payload()
        assert result is None

    def test_returns_first_valid_payload_among_multiple(self):
        """Should return the first request that has both id and doc_id."""
        scraper = _make_scraper()
        bad_req = _build_raw_request(variables={"count": 3}, doc_id="")
        good_req = _build_raw_request(variables={"id": "42"}, doc_id="7777")
        scraper.page_optional.driver.requests = [bad_req, good_req]

        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        result = scraper.get_init_payload()
        assert result["doc_id"] == "7777"


# ── format_data ───────────────────────────────────────────────────────────────

class TestFormatData:
    def _make_res_in(self):
        return [{
            "post_id": "987654321",
            "reaction_count": {"count": 42},
            "comment_rendering_instance": {"comments": {"total_count": 10}},
            "share_count": {"count": 5},
            "top_reactions": {"edges": []},
            "video_view_count": None,
        }]

    def test_output_contains_expected_keys(self):
        scraper = _make_scraper()
        scraper.requests_parser.context_list = ["Test post text"]
        scraper.requests_parser.owning_profile = [{"id": "123", "name": "Test"}]
        scraper.requests_parser.creation_list = [1700000000]

        result = scraper.format_data(
            res_in=self._make_res_in(),
            fb_username_or_userid="testuser",
            new_reactions=[{"讚": 30}]
        )
        assert len(result) == 1
        post = result[0]
        assert post["post_id"] == "987654321"
        assert post["username_or_userid"] == "testuser"
        assert post["post_url"] == "https://www.facebook.com/987654321"
        assert post["context"] == "Test post text"

    def test_deduplicates_posts_by_post_id(self):
        scraper = _make_scraper()
        scraper.requests_parser.context_list = ["Text A", "Text A duplicate"]
        scraper.requests_parser.owning_profile = [
            {"id": "123"}, {"id": "123"}
        ]
        scraper.requests_parser.creation_list = [1700000000, 1700000000]

        res_in = self._make_res_in() + self._make_res_in()
        result = scraper.format_data(
            res_in=res_in,
            fb_username_or_userid="testuser",
            new_reactions=[{}, {}]
        )
        # Duplicate post_id should be removed
        assert len(result) == 1

    def test_handles_missing_creation_time_without_crash(self):
        scraper = _make_scraper()
        scraper.requests_parser.context_list = ["Text A"]
        scraper.requests_parser.owning_profile = [{"id": "123"}]
        scraper.requests_parser.creation_list = []

        result = scraper.format_data(
            res_in=self._make_res_in(),
            fb_username_or_userid="testuser",
            new_reactions=[{}]
        )
        assert len(result) == 1
        assert result[0]["time"] is None


# ── process_reactions ─────────────────────────────────────────────────────────

class TestScraperProcessReactions:
    def test_delegates_to_requests_parser(self):
        scraper = _make_scraper()
        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        res_in = [{
            "top_reactions": {
                "edges": [
                    {"node": {"localized_name": "讚"}, "reaction_count": 10},
                ]
            }
        }]
        result = scraper.process_reactions(res_in)
        assert result == [{"讚": 10}]


class TestRequestsFlow:
    def test_no_creation_time_does_not_raise_index_error(self):
        scraper = _make_scraper()
        from fb_graphql_scraper.utils.parser import RequestsParser
        scraper.requests_parser = RequestsParser(driver=MagicMock())

        graphql_lines = [
            json.dumps({
                "data": {
                    "node": {
                        "feedback": {
                            "subscription_target_id": "p1",
                            "reaction_count": {"count": 1},
                            "top_reactions": {"edges": []},
                            "share_count": {"count": 0},
                            "comment_rendering_instance": {"comments": {"total_count": 0}},
                            "video_view_count": 0
                        }
                    }
                }
            }),
            json.dumps({"data": {"page_info": {"has_next_page": False}}})
        ]

        response = MagicMock()
        response.content = "\n".join(graphql_lines).encode("utf-8")

        with patch("fb_graphql_scraper.facebook_graphql_scraper.requests.post", return_value=response):
            result = scraper.requests_flow(
                doc_id="123",
                fb_username_or_userid="10001",
                days_limit=30,
                profile_feed=[],
                display_progress=False,
            )

        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["post_id"] == "p1"
        assert result["data"][0]["time"] is None
