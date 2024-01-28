from dotenv import dotenv_values


env = dotenv_values()


class AppSecrets:
    """Static Class to store secrets."""

    github_access_token = env.get("GITHUB_ACCESS_TOKEN")
    github_username = env.get("GITHUB_USERNAME")
    environment = env.get("ENVIRONMENT")
