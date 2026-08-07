# -*- coding: utf-8 -*-
import json
import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from fb_graphql_scraper.utils.utils import (
    find_feedback_with_subscription_target_id,
    find_message_text,
    find_creation,
    find_owning_profile,
    days_difference_from_now,
    is_date_exceed_limit,
)

# ── Fixtures ────────────────────────────────────────────────────────────────

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_graphql_response.json")

@pytest.fixture
def sample_graphql_data():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── find_feedback_with_subscription_target_id ────────────────────────────────

class TestFindFeedback:
    def test_finds_feedback_nested_in_story(self, sample_graphql_data):
        result = find_feedback_with_subscription_target_id(sample_graphql_data)
        assert result is not None
        assert result["subscription_target_id"] == "987654321"

    def test_returns_none_when_no_feedback(self):
        data = {"data": {"node": {"id": "123", "name": "no feedback here"}}}
        result = find_feedback_with_subscription_target_id(data)
        assert result is None

    def test_finds_feedback_in_list(self):
        data = [
            {"no_feedback": True},
            {
                "feedback": {
                    "subscription_target_id": "111",
                    "reaction_count": {"count": 5}
                }
            }
        ]
        result = find_feedback_with_subscription_target_id(data)
        assert result["subscription_target_id"] == "111"

    def test_returns_none_on_empty_dict(self):
        assert find_feedback_with_subscription_target_id({}) is None

    def test_returns_none_on_empty_list(self):
        assert find_feedback_with_subscription_target_id([]) is None


# ── find_message_text ─────────────────────────────────────────────────────────

class TestFindMessageText:
    def test_finds_text_in_story_message(self, sample_graphql_data):
        result = find_message_text(sample_graphql_data)
        assert result == "This is a test post content."

    def test_returns_none_when_no_message(self):
        data = {"data": {"node": {"id": "123"}}}
        result = find_message_text(data)
        assert result is None

    def test_finds_text_in_nested_list(self):
        data = {
            "edges": [
                {"node": {"story": {"message": {"text": "Hello from list"}}}}
            ]
        }
        result = find_message_text(data)
        assert result == "Hello from list"

    def test_returns_none_when_story_has_no_message_key(self):
        data = {"story": {"creation_time": 1700000000}}
        assert find_message_text(data) is None


# ── find_creation ────────────────────────────────────────────────────────────

class TestFindCreation:
    def test_finds_creation_time(self, sample_graphql_data):
        result = find_creation(sample_graphql_data)
        assert result == 1700000000

    def test_returns_none_when_missing(self):
        data = {"story": {"message": {"text": "no creation time"}}}
        assert find_creation(data) is None

    def test_finds_in_nested_list(self):
        data = {
            "items": [
                {"story": {"creation_time": 1699999999}}
            ]
        }
        assert find_creation(data) == 1699999999


# ── find_owning_profile ───────────────────────────────────────────────────────

class TestFindOwningProfile:
    def test_finds_owning_profile(self, sample_graphql_data):
        result = find_owning_profile(sample_graphql_data)
        assert result is not None
        assert result["id"] == "100044253168423"
        assert result["name"] == "Test User"

    def test_returns_none_when_missing(self):
        data = {"data": {"node": {"id": "123"}}}
        assert find_owning_profile(data) is None


# ── days_difference_from_now ──────────────────────────────────────────────────

class TestDaysDifferenceFromNow:
    def test_single_timestamp_7_days_ago(self):
        seven_days_ago = datetime.now() - timedelta(days=7)
        ts = int(seven_days_ago.timestamp())
        result = days_difference_from_now([ts])
        assert result == 7

    def test_picks_minimum_timestamp(self):
        # The function uses min(), so the oldest timestamp drives the result
        old_ts = int((datetime.now() - timedelta(days=30)).timestamp())
        new_ts = int((datetime.now() - timedelta(days=5)).timestamp())
        result = days_difference_from_now([new_ts, old_ts])
        assert result == 30

    def test_zero_days_for_now(self):
        ts = int(datetime.now().timestamp())
        result = days_difference_from_now([ts])
        assert result == 0


# ── is_date_exceed_limit ──────────────────────────────────────────────────────

class TestIsDateExceedLimit:
    def test_exceeds_limit(self):
        assert is_date_exceed_limit(max_days_ago=70, days_limit=61) is True

    def test_does_not_exceed_limit(self):
        assert is_date_exceed_limit(max_days_ago=30, days_limit=61) is False

    def test_exactly_at_limit(self):
        # max_days_ago == days_limit should NOT exceed (strictly greater than)
        assert is_date_exceed_limit(max_days_ago=61, days_limit=61) is False
