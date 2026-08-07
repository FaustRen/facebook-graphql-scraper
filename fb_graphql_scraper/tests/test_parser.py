# -*- coding: utf-8 -*-
import json
import os
import pytest
from unittest.mock import MagicMock
from urllib.parse import urlencode, quote

from fb_graphql_scraper.utils.parser import RequestsParser

# ── Fixtures ────────────────────────────────────────────────────────────────

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_graphql_response.json")

@pytest.fixture
def mock_driver():
    return MagicMock()

@pytest.fixture
def parser(mock_driver):
    return RequestsParser(driver=mock_driver)

@pytest.fixture
def sample_graphql_data():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_feedback():
    """A feedback dict that matches what collect_posts() expects."""
    return {
        "subscription_target_id": "987654321",
        "reaction_count": {"count": 42},
        "top_reactions": {
            "edges": [
                {"node": {"localized_name": "讚"}, "reaction_count": 30},
                {"node": {"localized_name": "哈"}, "reaction_count": 12},
            ]
        },
        "share_count": {"count": 5},
        "comment_rendering_instance": {"comments": {"total_count": 10}},
        "video_view_count": None,
    }


# ── extract_first_payload ─────────────────────────────────────────────────────

class TestExtractFirstPayload:
    def _build_payload(self, variables: dict, doc_id: str = "7890") -> str:
        """Build a URL-encoded payload string like Selenium-wire captures."""
        variables_json = json.dumps(variables)
        return urlencode({"doc_id": doc_id, "variables": variables_json})

    def test_extracts_doc_id_and_variables(self, parser):
        payload = self._build_payload({"id": "123", "count": 3}, doc_id="999")
        result = parser.extract_first_payload(payload)
        assert result["doc_id"] == "999"
        assert result["variables"]["id"] == "123"
        assert result["variables"]["count"] == 3

    def test_variables_parsed_as_dict(self, parser):
        payload = self._build_payload({"id": "456"})
        result = parser.extract_first_payload(payload)
        assert isinstance(result["variables"], dict)

    def test_handles_nested_variables(self, parser):
        nested = {"id": "789", "config": {"count": 10, "cursor": None}}
        payload = self._build_payload(nested, doc_id="111")
        result = parser.extract_first_payload(payload)
        assert result["variables"]["config"]["count"] == 10


# ── process_reactions ─────────────────────────────────────────────────────────

class TestProcessReactions:
    def test_maps_reaction_names_to_counts(self, parser):
        reactions_in = [
            {"node": {"localized_name": "讚"}, "reaction_count": 30},
            {"node": {"localized_name": "哈"}, "reaction_count": 12},
        ]
        result = parser.process_reactions(reactions_in)
        assert result["讚"] == 30
        assert result["哈"] == 12

    def test_empty_reactions(self, parser):
        result = parser.process_reactions([])
        assert result == {}

    def test_single_reaction(self, parser):
        reactions_in = [{"node": {"localized_name": "怒"}, "reaction_count": 1}]
        result = parser.process_reactions(reactions_in)
        assert result == {"怒": 1}


# ── collect_posts ─────────────────────────────────────────────────────────────

class TestCollectPosts:
    def test_collects_post_fields(self, parser, sample_feedback):
        parser.feedback_list = [sample_feedback]
        result = parser.collect_posts()
        assert len(result) == 1
        post = result[0]
        assert post["post_id"] == "987654321"
        assert post["reaction_count"]["count"] == 42
        assert post["share_count"]["count"] == 5
        assert post["comment_rendering_instance"]["comments"]["total_count"] == 10

    def test_empty_feedback_list(self, parser):
        parser.feedback_list = []
        assert parser.collect_posts() == []

    def test_multiple_posts(self, parser, sample_feedback):
        second_feedback = dict(sample_feedback, subscription_target_id="111111")
        parser.feedback_list = [sample_feedback, second_feedback]
        result = parser.collect_posts()
        assert len(result) == 2
        assert result[1]["post_id"] == "111111"


# ── parse_body (integration with fixture JSON) ────────────────────────────────

class TestParseBody:
    def test_parses_valid_body_content(self, parser, sample_graphql_data):
        parser._clean_res()
        body_content = [json.dumps(sample_graphql_data)]
        parser.parse_body(body_content)
        # Should have captured one feedback entry
        assert len(parser.feedback_list) == 1
        assert parser.feedback_list[0]["subscription_target_id"] == "987654321"
        # Should capture message text and creation time
        assert parser.context_list[0] == "This is a test post content."
        assert parser.creation_list[0] == 1700000000

    def test_ignores_invalid_json_lines(self, parser):
        """Lines that don't match the expected schema should be silently skipped."""
        parser._clean_res()
        body_content = [json.dumps({"data": {"other_key": {}}})]
        parser.parse_body(body_content)
        assert parser.feedback_list == []

    def test_accumulates_across_multiple_calls(self, parser, sample_graphql_data):
        parser._clean_res()
        body = [json.dumps(sample_graphql_data)]
        parser.parse_body(body)
        parser.parse_body(body)
        # Same data twice — should see two entries
        assert len(parser.feedback_list) == 2
