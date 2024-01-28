from dotenv import dotenv_values
import os


env = dotenv_values()


def get_env(key):
    """Get environment variable."""
    return os.getenv(key, default=env.get(key))


class AppSecrets:
    """Static Class to store secrets."""

    github_access_token = get_env("GITHUB_ACCESS_TOKEN")
    github_username = get_env("GITHUB_USERNAME")
    environment = get_env("ENVIRONMENT")
