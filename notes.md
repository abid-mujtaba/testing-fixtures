# Notes

## CI/CD

The `main` branch has comprehensive branch protections
including requiring a Pull Request.
This prevents `python-semantic-release` from pushing commits to the `main` branch when
it bumps the version (and modifies the changelog).

There are a couple of possible solutions to this.

Unfortunately both solutions require the branch protection to **allow** admin uers
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

1. In Github nagivate to (Personal) Settings > Developer Settings >
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

## CI/CD with SSH Deploy Key

Another solution is to use an SSH Deploy Key but that will require modifications to
the deploy Github Action.

*Note*: SSH Deploy keys use the "bypass branch protections" permission so
"Do not allow bypassing the above settings" should be **unchecked**
(in branch protection).

### Create SSH key

```bash
cd ~/.ssh
ssh-keygen -t ed25519 -a 100 -C "git@github.com:abid-mujtaba/testing-fixtures.git" -f testing-fixtures-deploy
```

*Note*: Do **not** set a passphrase.
*Note*: Github requires a comment (-C) equal to the SSH url of the repo for a
valid deploy key.

### Store keys

- Add the public key as the Deploy key to the repo (Settings > Security > Deploy Keys)
  and enable "Allow write access"
- Add the private key as a Github Actions secret in the repo
  (Settings > Security > Secrets and Variables > Actions)
  under the name `SSH_PRIVATE_KEY`

### Checkout code

By default the checkout action uses a one-time Github token.
Since we want to use a deploy key to push commits we need to ensure that
the same SSH key is used to checkout the code by configuring
the checkout action to use an `ssh-key`.

### SSH Agent

We want `python-semantic-release` to automatically use the SSH key when
it pushes the new commit.
We use the `webfactory/ssh-agent` action to setup an SSH agent with
the private Deploy key to make it available to `semantic-release` by default.

Also need to set `ignore_token_for_push = false` to force `semantic-release` to use ssh.

### Avoid workflow recursion

Since our release job is pushing a commit to the `main` branch there is a possibility
of workflow recursion.

Github Actions deals with this automatically **if**
the per-workflow Github token is used.
We are using a Deploy SSH key instead so will have to deal with recursion ourselves.

To avoid that we add an `if` condition to the `release` job so that it is skipped if
the top commit is authored by "Github Actions",
a user which the workflow configures before it pushes a deploy commit.

```yaml
release:
    if: github.event.commits[0].author.name != 'GitHub Actions'
```
