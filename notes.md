# Notes

## CI/CD

The `main` branch has comprehensive branch protections which are explicitly applicable
to Administrators as well.
This prevents `python-semantic-release` from pushing commits to the `main` branch when
it bumps the version (and modifies the changelog).

The solution might be to use an SSH Deploy Key but that will require modifications to
the deploy Github Action.

### Create SSH key

```bash
cd ~/.ssh
ssh-keygen -t ed25519 -a 100 -f testing-fixtures-deploy
```

*Note*: Do **not** set a passphrase.

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
