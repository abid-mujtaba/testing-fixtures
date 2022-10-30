# Tunable Fixtures

This repo contains an implementation of a "Tunable Fixture" and
a demo project where it is used to implement integration tests.

## Tunability

`pytest` fixtures are a powerful tool to separate setup+teardown from a test and
make it reusable.
However, they lack a straight-forward mechanism for passing arguments to them.
It is not uncommon to require that a specific piece of state be injected before
running a specific test.
A "tunable" fixture would solve this requirement.

## Decorators to the rescue

The objective is to create function that takes arguments which can be
applied as a decorator to test functions.

Example:

```python
@operation("square")
def test_compute_square(other_fixture, from_operation):
    ...
```

The `@operation("square")` returns a decorator which is applied to a test function.
That decorator performs setup and teardown around the test.
It **also** injects an argument `from_operation` into the test function.

Importantly, it does not interfere with the use of other fixtures which are
still being pulled in via arguments to the test function.

The implementation can be found in
[tests/integration/\_\_init__.py](tests/integration/__init__.py).

## Demo

To demonstrate this in action we have a REST server that:

- receives POST requests
- fetches data from a (postgres) database
- uses the fetched data to construct the response

This has been setup as a composable environment.
First build the local images: `docker-compose build`.
Then, run the tests: `docker-compose run --rm test`.

## Local Development

To make changes to this code base the recommendation is to use a virtual env:

```console
python3.10 -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
```

Your IDE should be able to now access this virtual env and
provide you with autocomplete, intellisense, etc.
