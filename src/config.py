import os
import re

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.config_vars = [
            # (var_name, env_name, default_value)
            # General
            ("port", "PORT", 6090),
            ("host", "HOST", "0.0.0.0"),
            ("logging", "LOGGING", False),
            ("logging_type", "LOGGING_TYPE", "INFO"),
            ("debug", "DEBUG", False),
            # Redis
            ("redis", "REDIS", False),
            ("redis_host", "REDIS_HOST", "db"),
            ("redis_port", "REDIS_PORT", 6379),
            ("redis_user", "REDIS_USER", None),
            ("redis_pass", "REDIS_PASS", None),
            ("screenshot", "ENABLE_SCREENSHOT", False),
            ("playwright_server", "PLAYWRIGHT_SERVER", None),
            ("screenshot_proxy", "SCREENSHOT_PROXY", False),
            # 1 day in seconds
            ("screenshot_cache_exp", "SCREENSHOT_CACHE_EXP", 86400),
            ("screenshot_timeout", "SCREENSHOT_TIMEOUT", 600000),
            ("screenshot_compress", "SCREENSHOT_COMPRESS", True),
            ("github_token", "GITHUB_TOKEN", None),
            ("api_ninjas_key", "API_NINJAS_KEY", None),
            ("rapidapi_key", "RAPIDAPI_KEY", None),
            ("translate_engine", "TRANSLATE_ENGINE", None),
            ("translate_url", "TRANSLATE_URL", None),
            ("shortener", "SHORTENER", False),
            ("shortener_url", "SHORTENER_URL", None),
            ("codebin", "CODEBIN", False),
            ("codebin_url", "CODEBIN_URL", None),
            # ("omdb_apikey", "OMDB_APIKEY", None),
        ]

        self.load_config()

    def infer_type(self, value):
        if value.lower() == "true" or value.lower() == "false":
            return bool
        elif re.match(r"^\d+$", value):
            return int
        else:
            return str

    def load_config(self):
        for var_name, env_name, default_value in self.config_vars:
            env_value = os.getenv(env_name)
            if env_value is not None:
                try:
                    value_type = self.infer_type(env_value)
                    if value_type == bool:
                        setattr(self, var_name, env_value.lower() == "true")
                    else:
                        setattr(self, var_name, value_type(env_value))
                except (ValueError, TypeError):
                    print(
                        f"Error: Environment variable '{env_name}' has invalid value '{env_value}'. Using default value."
                    )
                    setattr(self, var_name, default_value)
            else:
                setattr(self, var_name, default_value)


config = Config()
