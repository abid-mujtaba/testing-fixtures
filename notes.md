# Notes

## CI/CD

The `main` branch has comprehensive branch protections
including requiring a Pull Request.
This prevents `python-semantic-release` from pushing commits to the `main` branch when
it bumps the version (and modifies the changelog).

There are a couple of possible solutions to this.

Unfortunately both solutions require the branch protection to **allow** admin users
the ability to bypass branch protections.
To stop yourself from mistakenly pushing to the protected `main` branch from the CLI
one can use a simple hack: `git config --global branch.main.pushRemote no_push`.
This configures the remote for the `main` branch to the non-existent `no_push` remote.
Trying to `git push` will cause an error because the remote cannot be found.

## CI/CD with Personal Access Token

We will create a PAT (Personal Access Token) and
explicitly give it permission to "bypass branch protections".
The Github Action will have to be configured to use this specific PAT instead of
the auto-generated per-workflow Github Access Token which does **not** have
the required permission to push commits to a protected branch.

### Create Personal Access Token

1. In Github navigate to (Personal) Settings > Developer Settings >
   Personal Access Tokens > Fine-grained tokens > Generate new token
1. Limit repository access to just this repo.
1. Set the following Repository Permissions:

   1. Administration: Read and Write
   1. Contents: Read and Write
   1. Metadata: Read-only (Mandatory)

1. Leave everything else set to "No Access".
1. Click `Generate Token`
1. Copy generated token and place it in
   the repo's Github Actions Secrets with name `PAT`
   (Repo Settings > Secrets and variables > Actions > New repository secret)

### Checkout code

By default the checkout action uses a one-time Github token.
Since we want to use the PAT we need to configure the checkout action to use it.

```yml
- name: Checkout repository
  uses: actions/checkout@v2
  with:
    fetch-depth: 0  # semantic-release needs access to all previous commits
    token: ${{ secrets.PAT }}
```

### Avoid workflow recursion

Since our release job is pushing a commit to the `main` branch there is a possibility
of workflow recursion.

Github Actions deals with this automatically **if**
the per-workflow Github token is used.
We are using an admin PAT so will have to deal with recursion ourselves.

To avoid that we add an `if` condition to the `version` job so that it is skipped if
the top commit is authored by "semantic-release",
the user which python-semantic-release uses to push the bumped version commit.

```yaml
release:
    if: github.event.commits[0].author.name != 'semantic-release'
```

## PyPI Publication

1. Login to https://test.pypi.org/
1. Select your project
1. Click on the `Manage` button
1. In the left-pane click `Publishing`
1. Enable two-factor authentication (this is prerequisite for using Trusted Publishers)
1. Github is currently the only trusted publisher.
   Configure it:

   1. Owner: `abid-mujtaba`
   1. Repository: `testing-fixtures`
   1. Workflow name: `deploy.yml` (should be inside `.github/workflows/`)
   1. **No** environment set
