#!/usr/bin/env python
# encoding: utf-8

from fire import testutils

from logistics_api_adk_agent import __main__


class CoreTest(testutils.BaseTestCase):
    def test_version(self):
        with self.assertOutputMatches(stdout=".*"):
            __main__.fire.Fire(__main__.version, command=[])

    def test_version_help_info(self):
        with self.assertRaisesFireExit(0, regexp="显示当前版本"):
            __main__.fire.Fire(
                {"version": __main__.version}, command=["version", "--help"]
            )

    def test_bash_run(self):
        from logistics_api_adk_agent.__main__ import run

        res = run("请只回复你好")
        assert res == "你好"

        res = run("查看一下服务器状态")
        assert res == "你好"

    def test_run_server_status(self):
        from logistics_api_adk_agent.__main__ import run

        res = run("查看一下服务器状态 密钥 123456 如果正常 请返回 服务器状态正常")
        assert "服务器状态正常" in res
