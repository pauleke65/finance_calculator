from github import Github
from github import Auth

from app_secrets import AppSecrets

auth = Auth.Token(AppSecrets.github_access_token)

# Public Web Github
git_auth = Github(auth=auth)
