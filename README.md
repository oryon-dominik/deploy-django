# django deployment

a project from the *Virtual Autumn Sprint 2020* of the *Python Meeting Düsseldorf* - pyddf

to deploy a project to an external service

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
- gives an endpoint, e.g. /deploy-hash/
- generate a "secret-token" for the challenge/response
    
    import secrets
    secrets.hex(32)

## external service

GET /deploy/ -> get a "challenge" back (e.g a random number/string)

The response will get generated with "auth token" and "challenge" (e.g.: SHA(challenge + secret))

The external service does a POST to /deploy/ with the challenges response
