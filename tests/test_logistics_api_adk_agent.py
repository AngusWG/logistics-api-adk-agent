#!/usr/bin/python3
# encoding: utf-8

"""
test_logistics_api_adk_agent
----------------------------------

Tests for `logistics_api_adk_agent` module.
"""
import pytest

import logistics_api_adk_agent


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get("https://github.com/audreyr/cookiecutter-pypackage")


class TestLogistics_api_adk_agent:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_something(self, benchmark):
        assert logistics_api_adk_agent.__version__
        from logistics_api_adk_agent import __main__

        # assert cost time
        benchmark(__main__.version)
        assert benchmark.stats.stats.max < 0.01
