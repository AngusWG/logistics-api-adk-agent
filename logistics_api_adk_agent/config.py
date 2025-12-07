#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:03
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : config.py

import os
import typing

from dotenv import load_dotenv

load_dotenv()


class Config:
    project_name: str = "logistics_api_adk_agent"

    LOG_FORMAT: str = (
        "[%(asctime)s] [%(levelname)s]: "
        "%(message)s [%(pathname)s <%(lineno)d>]"
    )
    LOG_LEVEL: str = "INFO"
    log_file_dir: str = "."
    sentry_dns: str = None

    def __init__(self):
        """
        >>> Config()
        read config.yaml from...
        """
        print(f"=== Prepare {self.project_name} config start ===")

        # read config from env
        uppercase_vars = [var for var in vars(Config) if not var.startswith("__")]

        for var_name in uppercase_vars:
            _var_name = (self.project_name + "__" + var_name).upper()
            env_value = os.environ.get(_var_name)
            if env_value is not None:
                var_type = typing.get_type_hints(Config).get(
                    var_name, str
                )  # default string
                if var_type is bool and env_value.lower() in ("false", "f", "no", "0"):
                    env_value = False
                print(f"read from ENVIRON: {_var_name} = {env_value}")
                setattr(self, var_name, var_type(env_value))

        print(f"=== Prepare {self.project_name} config finish===")


conf = Config()
