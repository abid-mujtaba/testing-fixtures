# Project Evolution

We will be using this document to track the evolution of this project.

## PyCon US 2023

@abid-mujtaba conducted an Open Session on Sat Apr 22, 2023 (at 2pm) to discuss
"New approach to (pytest) fixtures."
Nearly 20 conference participants were present and
a broad consensus was achieved on the need for a new approach roughly along the lines proposed in this repo.
It was decided to approach the Pytest maintainers first before a new library was produced.

Subsequently, @pganssle connected @abid-mujtaba with @Zac-HD (Pytest core developer and
maintainer of Hypothesis) over lunch at the conference (afternoon of Sun Apr 23, 2023).
@Zac-HD was in general agreement with the proposal in this repo.
He suggested that a 2-pronged approach be taken:

1. Publish a library based on this repo
2. Investigate the pytest codebase to determine how hard it would be add functionality to disable native pytest fixtures

## Jul 2023

- Based on the feedback from PyCon @abid-mujtaba published `testing-fixtures` to PyPI.

## Nov 2023

- CI/CD was implemented including a full matrix of tests across 5 versions of Python and
  3 different OSes.
- Auto version bumping and auto publishing to PyPI was configured.
