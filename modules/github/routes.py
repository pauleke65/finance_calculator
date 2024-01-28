from flasgger import swag_from
from flask import jsonify

from modules.github.schema import GithubIssuesOut

from .main import git_auth


def github_routes(app):

    @app.get('/github/repos')
    @app.output(GithubIssuesOut(many=True))
    @app.doc(operation_id='GetGithubRepos', tags=['Github'])
    def get_repos():
        repos = []
        res = git_auth.get_user().get_repos()
        for repo in res:
            repos.append({'full_name': repo.full_name,
                         'description': repo.description})
        return repos
