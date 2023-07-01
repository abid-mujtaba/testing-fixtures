# Beyond Pytest Fixtures

This repo contains an implementation of a new approach to fixtures for use with
`pytest`.
In addition we demonstrate how to use these new fixtures in both unit and
integration tests.

## Project Evolution

The evolution of this project is being tracked in this [doc](./evolution.md).

## Advantages of `pytest` fixtures

`pytest` fixtures are extremely powerful and flexible.

- Provides a pythonic mechanism for setup, teardown, and injection of state into tests.
- Fixture scope is configurable allowing for heavy computation to be
  carried out once per test function (default), test module or session.
- Allows fixtures to be composed which sets up a causal relation between fixtures and
  sharing of state between multiple fixtures and the test function.

## Disadvantages of `pytest` fixtures

### Tunability

`pytest` fixtures lack a straight-forward mechanism for passing arguments to them from
the test function defition site.
It is not uncommon to require that a specific piece of state be injected before
running a specific test.
A "tunable" fixture would solve this requirement.

`pytest` solves this by *magically* allowing `pytest.mark.parametrize` values to be
passed through to a fixture being used by a test.
This is not obvious and uses a mechanism that is primarily used for
injecting multiple states into a test to create multiplicity.

### Importability

`pytest` recommends that fixtures be defined in a `conftest.py` file (a most non-obvious
name) and that they **not** be imported directly.
When tests are executed `pytest` parses `conftest.py` and magically inserts
the fixtures (setup, teardown, and interjection) into the test execution.
This is completely different from how the rest of Python operates and
is a source of great confusion to newcomers.

### Fixtures vs Injected Value

`pytest` fixtures overlap two distinct concepts when connecting a test function to
a fixture.
One is the name/handle to the fixture definition (generator function), and
the other is the variable inside the test function which is
bound to the value yielded by the fixture.

This over-use of a single name is evident every time one is choosing the name for
the fixture + variable.
Does one name it for the variable or for the operation that the fixture carries out
whose side-effect is the value in the varible e.g.
`add_portfolio` vs `portfolio_name`.

### Type Annotation

The way `pytest` *registers* fixtures and then *injects/interleaves* them into/with
test functions means it is practically impossible for a type engine to match and
enforce types between the fixture definition and the value injected into
the test function.

This is a source of considerable frustration for anyone who has gone through the
effort to annotate their code and their tests.

## Prototype

We provide a prototype for a new type of fixtures beyond what is provided by `pytest`.

### Objectives

- Works seamlessly with `pytest`.
- Importable from another module (no more `conftest.py`).
- Composable.
  One fixture can be connected to another fixture and recieve a value from it.
- Tunable.
  Fixtures definitions can declare parameters.
  These parameters can either be provided at **either**
  the test definition site **or**
  inside the fixture definition module.

  The value(s) provided to the parameter(s) will remain consistent throughout
  the execution of any given test.
  The same value will be visible to all participating entities:
  the test function and all fixtures composed with said fixture.
- Fully typed and type-aware.
  Provides enforceable bindings between fixture definitions,
  values injected into fixtures, and
  values injected from them into test functions.

### Interface

To achieve **all** of the objectives listed above the interface for these fixtures is
slightly more verbose than `pytest` fixtures while
being significantly less magical.

The following four decorators are provided for defining these fixtures:

1. `@fixture`: Applied to a fixture definition (one-shot generator function).
   Creates an instance of the `Fixture` class.
   **This instance is both a decorator as well as a
   reusable and reentrant context manager.**

   This instance is applied as a decorator to test functions and injects
   the yielded value into it.

   Example (extracted from `tests/unit/utils.py`):

   ```python
   @fixture
   def fixture_b(b1: Bi1, b2: Bi2) -> FixtureDefinition[Bo]:
       """A fixture that takes injected value from the test function decoration."""
       yield Bo(b1=b1, b2=b2)
   ```

   *Note* One can use `NewType` and `TypedDict` to constrain the fixture parameters and
   the value it yields which allows for tightly binding the yielded value
   to any location where it is used (test function or composed fixture).
   Similarly the `FixtureDefinition[]` generic type constrains how the fixture is
   allowed to be used.

   Each instance has a `.set()` method which is used to provide values for
   any parameters declared in the fixture definition.

   `.set()` can be called on either the test function decoration site,
   inside the module defining the fixture,
   or while composing the fixture with another.

   Examples (extracted from `tests/unit/utils.py` and
   `tests/unit/test_new_fixtures.py`):

   ```python
   @fixture_b.set(Bi1(42), Bi2(3.14))
   def test_b(b: Bo) -> None:
       """Test parametrized fixture_b in isolation."""
       assert b == {"b1": 42, "b2": 3.14}
   ```

   or

   ```python
   @fixture
   @compose(fixture_b.set(Bi1(13), Bi2(1.44)))
   def fixture_c(b: Bo) -> FixtureDefinition[Co]:
       """A fixture that takes an injected value from ANOTHER fixture."""
       yield Co(c=b)
   ```

   All fixture composition and test decoration creates a strict ordering of when the
   fixture's context manager is entered and exited.
   Only the value at the first entry is available throughout the execution of a single
   test.

1. `@compose`: A function that takes a single argument which must be an instance of
   `Fixture` and returns a decorator that is applied to another fixture definition.
   Designed to be applied **before** the fixture definition is wrapped inside
   `@fixture` (don't worry,
   the type system will shout at you if you get the order wrong).

   The value yielded by the composed fixture is injected as the first parameter of
   the decorated fixture definition.
   It essentially creates a simpler fixture definition with one less parameter.

   Example:

   ```python
   @fixture
   @compose(fixture_b.set(Bi1(13), Bi2(1.44)))
   def fixture_c(b: Bo) -> FixtureDefinition[Co]:
       """A fixture that takes an injected value from ANOTHER fixture."""
       yield Co(c=b)
   ```

   The composed fixture can also have its value set from the test site but
   be available to the composition.

   Example:

   ```python
   @fixture
   @compose(fixture_b)
   def fixture_g(b: Bo, g: Gi) -> FixtureDefinition[Go]:
       """Fixture that uses a late-injected fixture_b and a value from the test site."""
       yield {"b": b, "g": g}

   @fixture_b.set(Bi1(56), Bi2(9.7))
   @fixture_g.set(Gi(41))
   def test_g(g: Go, b: Bo) -> None:
       """Inject args into fixture from test site and trickle down to pulled in fixture."""
       assert b == {"b1": 56, "b2": 9.7}
       assert g == {"b": b, "g": 41}
   ```

1. `@noinject`: Used at the test definition decoration site to wrap fixtures.
   The wrapped fixture's yielded values will **not** be injected into the test function.

   Example:

   ```python
   @noinject(fixture_b.set(Bi1(75), Bi2(2.71)))
   def test_b_no_injection() -> None:
       """The value yielded by fixture_b is NOT injected into the test."""
   ```

   The type engine will understand *not* injecting and validates accordingly.

1. `@compose_noinject`: Applied to composed fixtures to *stop* them from injecting
   their yielded value into the fixture they are composed with.

   Example:

   ```python
   @fixture
   @compose_noinject(fixture_b.set(Bi1(39), Bi2(8.1)))
   def fixture_h(h: Hi) -> FixtureDefinition[Ho]:
       """Fixture that uses a composed fixture_b but NOT its yielded value."""
       yield Ho(h=h)
   ```

   Again, the type engine is aware of the mechanics.

## Implementation

The implementation can be found in [testing.fixtures](./testing/fixtures).
It consists of nested decorators, modified context managers, and parameter injection,
all fully typed.

## Demo

### Integration Tests

To demonstrate this in action we have a REST server that:

- receives POST requests
- fetches data from a (postgres) database
- uses the fetched data to construct the response

This has been setup as a composable environment.
First build the local images: `docker-compose build`.
Then, run the tests: `docker-compose run --rm test`.

### Unit Tests

We have also provided a number of unit tests, unrelated to the REST server application,
which focus on demonstrating all the possible permutations of fixture usage,
composition, and state injection at both the test and fixture definition site.

## Local Development

To make changes to this code base the recommendation is to use a virtual env:

```console
python3.11 -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
```

Your IDE should be able to now access this virtual env and
provide you with autocomplete, intellisense, etc.

## How to Deploy

1. Build the package: `python3.11 -m build`
   This will create the source tarball and wheel in the `dist/` folder.

2. Deploy to pypi: `python3.11 -m twine upload dist/*`
   Enter your pypi username and password.
