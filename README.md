# django deployment

a project from the *Virtual Autumn Sprint 2020* of the *Python Meeting Düsseldorf* - pyddf


## CI/CD -resources
Implement a CI/CD flow for a django project using GitHub Actions including deployment to a root server with GitHub Secrets.
Resources
Setting up Github Actions with Django and Postgres: https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/
How to safely use GitHub Actions in organizations: https://humanwhocodes.com/blog/2020/07/safely-use-github-actions-in-organizations/
Manage secrets and more with the GitHub Actions API: https://github.blog/2020-02-06-manage-secrets-and-more-with-the-github-actions-api/
GitHub Developer Secrets: https://developer.github.com/v3/actions/secrets/


## Idea deployment API

### external service

- e.g github-action or local script -> pushes deployment over the API
- saves the secret-token to answer the challenge/response

### django project

the project to deploy

- implements our reusable app as module
- gives 


