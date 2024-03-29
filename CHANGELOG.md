# CHANGELOG



## v0.4.1 (2024-01-14)

### Fix

* fix: remove unnecessary noqa (#54)

- CI has started to complain about this ([`2387b18`](https://github.com/abid-mujtaba/testing-fixtures/commit/2387b186ef7b5fed05dab521465fd1ba89f48e98))


## v0.4.0 (2023-12-09)

### Chore

* chore: refactor tox requirements (#52)

- Put the test deps in requirements-test.txt.
- Put the lint deps in requirements-lint.txt and also include
  requirements-test.txt in it.
- Create a new dev-py312 environment which uses an editable install.
  This will serve as the development environment for VS Code. ([`d29cb8f`](https://github.com/abid-mujtaba/testing-fixtures/commit/d29cb8f46fc9d7567fbcf1c4991aa87dbd7f2dc7))

### Documentation

* docs: added notes on evolution uptill Nov 2023 (#51)

documented the new CI/CD pipeline ([`748e2c8`](https://github.com/abid-mujtaba/testing-fixtures/commit/748e2c8a98cf4355cefab41708b3334c10cfc151))

### Feature

* feat: add commonly used utility fixtures (#53)

- add a new `.utils` submodule
- add create_temp_dir and create_temp_cwd utility fixtures
- refactor vscode settings
- make mypy strict ([`9edf0f4`](https://github.com/abid-mujtaba/testing-fixtures/commit/9edf0f4e7dccd0f77f4042a3831155d12cfd1f9c))

### Style

* style(core): apply new ruff format rules (#50)

ruff has acquired a new format rule where even function definitions with
a single argument that are split across multiple lines should have a
trailing comma after that single argument ([`ae2c5fc`](https://github.com/abid-mujtaba/testing-fixtures/commit/ae2c5fc0248939bf32f2577b4a677060e36614f8))


## v0.3.0 (2023-12-02)

### Ci

* ci: add semantic-pr workflow (#47)

Ensure that the PR title follows semantic commit style
otherwise version bumping won&#39;t work because
it looks at the commit titles to figure out if a bump is required and
the category of bump ([`509ac27`](https://github.com/abid-mujtaba/testing-fixtures/commit/509ac27238db5f57ef58548f847fbb1b0682adb3))

### Feature

* feat: bump version to include deps (#49)

- Need a commit using semantic convention to trigger a bump version to
  pick up the latest change which was to add typing-extension as a dep ([`9d585d8`](https://github.com/abid-mujtaba/testing-fixtures/commit/9d585d827994dfa853e08738b64291b48218f6cb))

### Unknown

* Bump version to incorporate new deps (#48)

feat: bump version to incorporate new deps

- typing-extensions was added as a dependency but was not incorporated
  because the commit didn&#39;t have semantic style.
- we have added a github action to validate that can no longer happen
- still need to bump the version to include the new dep ([`6ba5364`](https://github.com/abid-mujtaba/testing-fixtures/commit/6ba536441a62bcec013f3f9c00b43b24cdf10773))

* Add typing-extensions as dependency (#46)

Used by library to support lower versions of Python ([`7d2b4a3`](https://github.com/abid-mujtaba/testing-fixtures/commit/7d2b4a39b0172fe257bcc43bbf02fca2b8f03b0d))


## v0.2.4 (2023-11-13)

### Fix

* fix: remove unnecessary fetch-depth config (#45)

- the only component of CI/CD that needs access to the full commit history is
the version bumping logic (sematnic-release)
- bring the setup-python actions into consistency with each other ([`16fad96`](https://github.com/abid-mujtaba/testing-fixtures/commit/16fad96401f08cac6a21475bf591833f2c81f6c3))


## v0.2.3 (2023-11-13)

### Ci

* ci: format config (#43)

no functional change just add some whitespace and
remove unnecessary name of the checkout step ([`40e8fe2`](https://github.com/abid-mujtaba/testing-fixtures/commit/40e8fe2b360d7cb604b940d5a3dda6062b9857f0))

### Fix

* fix: use ruff check and format (#44)

* ci: add ruff (check &amp; format), remove black

- ruff check is fantastic
- ruff format is a drop-in replacement for black (in particular the upcoming preview)
  the only places where ruff disagrees with black I agree with the former

* ci: configure ruff

- select all rules
- disable the 4 rules globally that conflict with ruff format
- disable certain rules on a per-file basis
  - assert is allowed in tests
  - we are using print in the unit tests to track execution

* fix: ruff errors

fix all errors detected by ruff after we turned on nearly all the rules

* ci: configure vscode to use ruff

helps find and fix ruff errors ([`c1b1526`](https://github.com/abid-mujtaba/testing-fixtures/commit/c1b1526b1e9eec471888f94d750b82bb414e7a14))


## v0.2.2 (2023-11-12)

### Fix

* fix: semantic-release committer name (#42)

the switch to the upstream semantic-release action meant that
the committer name changed from semantic-release to github-actions

we explicitly configure the action to use the former name since that is
what is expected by the other publish workflow ([`480cf2a`](https://github.com/abid-mujtaba/testing-fixtures/commit/480cf2a68f11cd6b60a78a3d23187a24dcc14ff5))


## v0.2.1 (2023-11-12)

### Documentation

* docs: update notes (#39)

- remove discussion of SSH Deploy Keys
- add discussion of trusted publisher config in PyPI ([`efd7599`](https://github.com/abid-mujtaba/testing-fixtures/commit/efd759917e7a1e79a7fa9c252185cffc3f348d81))

### Fix

* fix: typo in version workflow (#41)

Typo in the workflow yaml ([`0f18bbb`](https://github.com/abid-mujtaba/testing-fixtures/commit/0f18bbb3c382cc7d894772044fc113139085d6ef))

* fix: use upstream semantic-release action (#40)

* ci: refactor build command

use the more popular `python -m build` instead of `pyproject-build`
since they are exactly equivalent

* fix: switch to upstream semantic-release action

trying once again with the admin PAT and an explicit skip_build option
since the primary problem with the upstream action was failure to build
but we no longer need to build just to bump and release the new version ([`75b7cad`](https://github.com/abid-mujtaba/testing-fixtures/commit/75b7cadaf4d531098fa42c6edc0efc8fc386c731))


## v0.2.0 (2023-11-12)

### Feature

* feat: publish to pypi (#38)

- rename file from deploy.yml to publish.yml since publication is
  the more accurate verb when it comes to Python and PyPI
- add additional config to publish.yml for publising to PyPI if
  publication to TestPyPI succeeds
- remove dead code from pyproject.toml ([`f8a6cea`](https://github.com/abid-mujtaba/testing-fixtures/commit/f8a6cea0eab6cdf1ebd75b861bbfeec2b39ede67))


## v0.1.10 (2023-11-12)

### Fix

* fix: version bump (#37)

- fix typo in semantic-release config for specifying location of version inside the project
- Add --skip-build since semantic-release does not need to build the project to bump the version
- Remove build specific config from semantic-release ([`5627ed1`](https://github.com/abid-mujtaba/testing-fixtures/commit/5627ed1bb064702d14b756d429abd4cba92aff00))


## v0.1.9 (2023-11-12)

### Fix

* fix: deploy condition (#36)

there was a typo in the if condition in the test-release job
the correct context is github.event (singular) ([`aa58e98`](https://github.com/abid-mujtaba/testing-fixtures/commit/aa58e987b5cb6ad9c0621f89d0d2dd2459afae50))


## v0.1.8 (2023-11-12)

### Fix

* fix: add deploy workflow (#35)

- refactor old deploy to the version workflow since it was technically
  all about bumping the version using semantic-release
- add an actual deploy workflow which currently is publishing only to Test PyPI ([`2f14668`](https://github.com/abid-mujtaba/testing-fixtures/commit/2f14668bc5fa0b52307692cad7b1f116b75db072))


## v0.1.7 (2023-11-11)

### Fix

* fix: disable cancel in progress (#34)

unfortunately even though cancel-in-progress when
a new commit is pushed to a branch while the previous build is running
works BUT it sends an automated email which is indicative of a failure
while this should technically be considered normal/desired behavior ([`632b84f`](https://github.com/abid-mujtaba/testing-fixtures/commit/632b84f68dc8563053a92eb36630d873a25fe316))


## v0.1.6 (2023-11-11)

### Fix

* fix: revert upstream semantic-release (#33)

The upstream python-semantic-release Github Action is unable to build
using pyproject-build ([`ec7e2c1`](https://github.com/abid-mujtaba/testing-fixtures/commit/ec7e2c1a0380eef33124e753b5429b63e837b172))

* fix: switch to using upstream semantic-release action (#32)

rather than install semantic-release and run it by hand we attempt to use
the upstream python-semantic-release action ([`2fabb08`](https://github.com/abid-mujtaba/testing-fixtures/commit/2fabb0871a6121e993a87eb0e41d8130c7362ae2))


## v0.1.5 (2023-11-11)

### Fix

* fix: use admin pat (#31)

- Trying out the admin PAT approach where we use a PAT with Admin
  permissions in place of the auto-generated per-workflow Github Token
- Document this new PAT approach in the notes
- Configure the CI check to run on all branch pushes but NOT on tag push ([`72315db`](https://github.com/abid-mujtaba/testing-fixtures/commit/72315db1412d67b3e6650c641dff2b38a5a75ef5))


## v0.1.4 (2023-11-10)

### Fix

* fix: semantic-release CLI args (#30)

fix typo in the CLI args passed to semantic-release
the new args are specific to the &#39;version&#39; subcommand ([`829ddb0`](https://github.com/abid-mujtaba/testing-fixtures/commit/829ddb00eb3427f2cdb43abcb436361a59b47c80))

* fix: split semantic release into two (#29)

attempting to commit and push in one step (using the Deploy key) and
creating the Github release in another step (using the Github Token) ([`d7f2974`](https://github.com/abid-mujtaba/testing-fixtures/commit/d7f2974af4b5b2b41da28d86c7c14a595a93a231))

* fix: gh-token in semantic-release (#28)

the per-workflow github-token is not available by default as an env var
specify it explicitly using the `env` config section
since we are going to be specifying it any way might as well make it available as GH_TOKEN, the default env var expected by semantic release ([`f1cfdab`](https://github.com/abid-mujtaba/testing-fixtures/commit/f1cfdab661b8af072612ba0bcd7134e301b8f8f5))


## v0.1.3 (2023-11-07)

### Fix

* fix: specify github token env var (#27)

GH Action makes the per-workflow GITHUB_TOKEN available as an env var while by default semantic-release looks for GH_TOKEN
since we will be using the GITHUB_TOKEN to create a new release we add write contents permission to the token ([`f04af65`](https://github.com/abid-mujtaba/testing-fixtures/commit/f04af651f33544ad7d2d6213f13a1c9eaf76e312))


## v0.1.2 (2023-11-07)

### Ci

* ci: increase semantic-release verbosity (#25)

the creation of github release is failing while the new commit is being correctly pushed up
increase semantic-release verbosity to figure out what is broken ([`a203260`](https://github.com/abid-mujtaba/testing-fixtures/commit/a20326034de77e28139fb45a135b4638a9b77f6a))

### Fix

* fix: add debug step after semantic-release (#26)

curious to see if a step will run after the previous one fails ([`bd37aba`](https://github.com/abid-mujtaba/testing-fixtures/commit/bd37aba4c3ef6492b964dc7011241b8f6b42811b))


## v0.1.1 (2023-11-07)

### Fix

* fix: author of deploy commit for skipping (#24)

semantic-release creates commits with author &#34;semantic-release&#34; which is what we need to use for skipping workflow for the deployed commit ([`98ed610`](https://github.com/abid-mujtaba/testing-fixtures/commit/98ed610380a5d83d96126f784201ce477bb9217b))


## v0.1.0 (2023-11-07)

### Ci

* ci: add preliminary deploy workflow (#8)

- Add config for semantic-release
- Use semantic-release to build package and create Github release ([`4c06108`](https://github.com/abid-mujtaba/testing-fixtures/commit/4c0610894bf843110172aba83cbc6e96c07bacde))

### Documentation

* docs: clarify branch protections required for deploy keys

Deploy keys use the &#34;bypass branch protections&#34; permission which needs to be enabled in branch protecton for the key to work ([`c173c1c`](https://github.com/abid-mujtaba/testing-fixtures/commit/c173c1c255efeb5e2e8cb329b629416f68374212))

### Feature

* feat: use deploy ssh key (#21)

the per-workflow Github token is not working because the main branch has branch protections (including for admininstrators) while the github token has the saame permissions as the user who launched the workflow ([`19757f7`](https://github.com/abid-mujtaba/testing-fixtures/commit/19757f7694978d9ba79da35753c846aa939c9549))

* feat: semantic-release version only (#20)

the publish command does not version first and we are going to be uploading the dist differently anyway ([`ab0ff0a`](https://github.com/abid-mujtaba/testing-fixtures/commit/ab0ff0ada9a06101d4c51c48dbdc0e197e72783c))

* feat: make semantic-release verbose (#19)

the command passes in CD but doesn&#39;t seem to be doing much
increase verbosity to investigate ([`747efee`](https://github.com/abid-mujtaba/testing-fixtures/commit/747efeee9f811179030ec77fc76cba051a678277))

* feat: use default build command (#15)

the specified build commands are not working with python-semantic-release so we are going to try the default build command ([`359fae3`](https://github.com/abid-mujtaba/testing-fixtures/commit/359fae304e751c792cd40a59c021505e6a6c01a2))

* feat: use semantic-release action (#11)

- semantic-release comes with its own Github Workflow action which
simplifies the setup
- add explicit build step
- rename job to release ([`de87e32`](https://github.com/abid-mujtaba/testing-fixtures/commit/de87e32cc56c59ab6a5208c7a0ce26b53672b7a2))

### Fix

* fix: add comment to deploy key (#23)

it seems Github requires deploy keys to have a comment equal to the SSH url of the repo it belongs to ([`2a9fa2b`](https://github.com/abid-mujtaba/testing-fixtures/commit/2a9fa2b88ff016f53b0037b250821cfa757f7589))

* fix: configure git after checkout (#22)

it is not possible to configure git before the code has been checked out (which creates the .git folder) ([`4125fa4`](https://github.com/abid-mujtaba/testing-fixtures/commit/4125fa4575f52557608f63364c90d3980e48f5e7))

* fix: semantic-release command (#18)

fix typo ([`60f7559`](https://github.com/abid-mujtaba/testing-fixtures/commit/60f7559510ef4298fc16891d51b7b7d9d1111694))

* fix: semantic-release config (#16)

misspelled config key which is being replaced with a better one
re-add the build command (removing it removes the build step) ([`e0bd802`](https://github.com/abid-mujtaba/testing-fixtures/commit/e0bd8029cceaa24b9726f32a73a862104f2f534c))

* fix: semantic-release build-command (#14)

- `python -m build` is not working in CD, possibly because of a &#34;build&#34; folder being created
- The build package comes with a `pyproject-build` script that does the same thing so switching to that instead ([`5172856`](https://github.com/abid-mujtaba/testing-fixtures/commit/517285688dd64e8b4b3f03b1d867716b90d74bf1))

* fix: install release prereqs (#13)

- the build package is required by semantic-release to use `python -m build` ([`0d5d6b4`](https://github.com/abid-mujtaba/testing-fixtures/commit/0d5d6b461d36a52915b79837fed1ddcca62eb49b))

* fix: semantic-release build command (#12)

- in CI (Github Action) the interpreter is available as just plain &#39;python&#39;
- remove the explicit build step since semantic-release will be doing the building AFTER it has bumped the version ([`86421d3`](https://github.com/abid-mujtaba/testing-fixtures/commit/86421d3c2d8a37e2146577a9760aa30a26cf426f))

* fix: semantic-release configuratioon (#10)

- semantic-release expects the github token to be present in the GH_TOKEN env var
- Configure the git user and email to belong to Github Actions so that the commit pushed by semantic-release is correctly attributed ([`8b7e9bb`](https://github.com/abid-mujtaba/testing-fixtures/commit/8b7e9bb5d8febb92aa36e4e9e21a603fbfe6c838))

* fix: trigger for deploy workflow (#9)

Since the deploy workflow is completely separate instead of using
the if syntax we can specify that the workflow is triggered &#34;on&#34;
the &#34;push&#34; event filtered to the &#34;main&#34; branch ([`b02afc9`](https://github.com/abid-mujtaba/testing-fixtures/commit/b02afc905b6cf0d7462e0608fc1623212038cbe8))

### Unknown

* Use semantic-release directly (#17)

instead of by the upstream action which we can&#39;t seem to be able to make work ([`372100b`](https://github.com/abid-mujtaba/testing-fixtures/commit/372100b839c7a89d91d2b6d92d12e1ce30874bea))

* Add py38 and py39 to tox and CI (#6)

- Use typing_extensions to pull in back-ported Concatenate and ParamSpec
- Switch to typing.Tuple and typing.Dict since py38 does not have
  support for using tuple and dict as types ([`9a36178`](https://github.com/abid-mujtaba/testing-fixtures/commit/9a36178e42ed66f66c941a7a9360462c04b05542))

* Run docker compose test in ci (#5)

- Configure Github Actions to build the containers and then run the test
  container, all inside the `example` folder.
- Switch to python3.12 in all the docker images.
- Switch to explicit python:3.12.0-slim-bookworm base image.
  Using a non-explicit python:latest image (where the architecture has
  to be inferred on the platform was breaking in CI) ([`cd9c1a1`](https://github.com/abid-mujtaba/testing-fixtures/commit/cd9c1a12aaf1e582ba9d6bd4acde28aba12a637d))

* Add tox linting to CI (#4) ([`78eb1ba`](https://github.com/abid-mujtaba/testing-fixtures/commit/78eb1ba95509f7496c9c3ed88cdf930ea54f74c1))

* Configure tox Github Action

- Add mypy to main tox environments since verifying the type annotations
is a primary function of this repo. ([`2d52176`](https://github.com/abid-mujtaba/testing-fixtures/commit/2d52176fa04eeab2deb802245fa21becd825e6d1))

* Enable mypy

- The ParamSpec error in mypy has been resolved so we have re-enabled
  mypy.
- Ignore pylint no-member error.
- Add support for Python 3.12 ([`222c967`](https://github.com/abid-mujtaba/testing-fixtures/commit/222c96761025bbc8b076247f25a046542f04a588))

* Update example to build and use testing.fixtures ([`7077d15`](https://github.com/abid-mujtaba/testing-fixtures/commit/7077d1553b8687a82759b20a97e89a2fe137ef47))

* Added info on PyPI publication to evolution doc ([`8d776e7`](https://github.com/abid-mujtaba/testing-fixtures/commit/8d776e7fdf5f7406c36fcb091c3de3f8340dcaea))

* Add deployment instructions ([`e0fd659`](https://github.com/abid-mujtaba/testing-fixtures/commit/e0fd659a5036fda67dfa14bb11529e2766973655))


## v0.0.2 (2023-07-01)

### Unknown

* Rename project (use hyphen) and add home page (github) ([`127628e`](https://github.com/abid-mujtaba/testing-fixtures/commit/127628e511612b437e6a05fc3273f2f8f2a56549))

* Update pyproject in preparation for pulication ([`8edbe6c`](https://github.com/abid-mujtaba/testing-fixtures/commit/8edbe6c2c6127582af6016c3e7d4525c64f9cfbf))

* Add py.typed to testing.fixtures package ([`ee77885`](https://github.com/abid-mujtaba/testing-fixtures/commit/ee77885cfa2c05788795103c7382cb7c08f20e13))

* Fix pylint and black errors ([`8573ce1`](https://github.com/abid-mujtaba/testing-fixtures/commit/8573ce161ea9b0460cf2102d97eb713e07a160fe))

* Add tox (to test py310 and py311) and to lint ([`08a0a75`](https://github.com/abid-mujtaba/testing-fixtures/commit/08a0a75257334ee6480526a12c65ce140784df87))

* Refactor to use src/ and add pyproject.toml ([`dd3b960`](https://github.com/abid-mujtaba/testing-fixtures/commit/dd3b96058dbbcd3694956ddec972190dfa805912))

* Refactor fixtures.py to testing.fixtures ([`c10a8cf`](https://github.com/abid-mujtaba/testing-fixtures/commit/c10a8cf4dec198ae54f46cbc24b557a71fe7cba0))

* Switch to python3.11 ([`50cda61`](https://github.com/abid-mujtaba/testing-fixtures/commit/50cda61a111cae049f8dedb1798f280d98f7d47d))

* Switch to netcat-traditional to install nc ([`4d0b134`](https://github.com/abid-mujtaba/testing-fixtures/commit/4d0b1342e40d6a0171e6b186afee529ddd949150))

* Move integration test example into separate folder

- Preparing to publish this package.
  The package will have its own pyproject.toml and `src/` folder so
  we wish to avoid confusion with the same structure for the example. ([`903ca8a`](https://github.com/abid-mujtaba/testing-fixtures/commit/903ca8a2a510b4f6878d462efa2f7d67f10c6f4f))

* Add link to evolution doc in README ([`a5bc7f1`](https://github.com/abid-mujtaba/testing-fixtures/commit/a5bc7f1bcefb337aaea9b8a9afb68c50f668b6f8))

* Add doc tracking evolution of project ([`7a9af05`](https://github.com/abid-mujtaba/testing-fixtures/commit/7a9af0569f576ab4fd35cf8a7d1147ad12e8f6c8))

* Considerable overhaul of the documentation ([`38eaebd`](https://github.com/abid-mujtaba/testing-fixtures/commit/38eaebd38cc79e92ec87062d6b897c83a0f5baa9))

* Add unit tests to the test container command ([`4effbf3`](https://github.com/abid-mujtaba/testing-fixtures/commit/4effbf3bc929e0fbdd81e9012265a235f5c96f66))

* Refactor integration tests to use new fixtures

- Remove old implementation of tunable-fixtures.
- Refactor commong utilities into a separate utils module. ([`fa41673`](https://github.com/abid-mujtaba/testing-fixtures/commit/fa41673a0aec33bc2e7f96cf6f0bba9a217f8ef7))

* Move fixture module to top-level while allowing import from the tests ([`5e151d7`](https://github.com/abid-mujtaba/testing-fixtures/commit/5e151d763872f3fd72c21de7dc1fdac8f6730520))

* Add compose_noinject function ([`42691be`](https://github.com/abid-mujtaba/testing-fixtures/commit/42691bea4e0cf1c4e3bab26a7bb654fcf9ec2bdf))

* Add noinject function for wrapping fixtures so that no injection occurs ([`230b6cd`](https://github.com/abid-mujtaba/testing-fixtures/commit/230b6cd143e0be480c455f88af13fd01f90627c2))

* Add vscode config ([`5c596fe`](https://github.com/abid-mujtaba/testing-fixtures/commit/5c596fe0ed1ba8e8d6e267bf2b64b882251bb581))

* Catch error caused by unordered fixtures and reset entries count (for later use) before re-raising error ([`9e4b84e`](https://github.com/abid-mujtaba/testing-fixtures/commit/9e4b84e9ee1cb92d37ede128d86ba729c95fbc5f))

* Add examples (marked as xfail) of using fixtures in the incorrect order) ([`10843e0`](https://github.com/abid-mujtaba/testing-fixtures/commit/10843e0d7787cc6171f8b0f5ac70f50da9eff5ad))

* Add test where fixture is used both at test and via composition and state is applied at composition ([`c8aede5`](https://github.com/abid-mujtaba/testing-fixtures/commit/c8aede56e2e9565dddc07383eebc7db7845b3243))

* Refactor (kw)args resetting in fixture

- Reset immediately after the (kw)args have been closed over (in a
  closure) since at that point the values have been cached at the
  correct location. ([`e41d90a`](https://github.com/abid-mujtaba/testing-fixtures/commit/e41d90af55f482372ffa126263b644f7e3d19389))

* Heavy refactor of Fixture

- Remove definition args and kwargs from Fixture initialization.
- Create .set() (and .reset()) methods to allow injecting definition
  args and kwargs into the fixture at any stage.
  Closures have been used to cache these arguments at both the test
  wrapper and the closure wrapper to ensure that state is consistent
  across a test run. ([`f1081c2`](https://github.com/abid-mujtaba/testing-fixtures/commit/f1081c2abf294fd47041ebd865c01645d885bea2))

* Comment out fixture_g in preparation for a fixture refactor ([`4ba0b6c`](https://github.com/abid-mujtaba/testing-fixtures/commit/4ba0b6ce88c35d8d54273dd9777db60fc03fd52e))

* Make the Fixture class generic over ParamSpec D (clearer indication of intent) ([`c949238`](https://github.com/abid-mujtaba/testing-fixtures/commit/c949238c70996f5d8395a14f2dfd0706c57f2a0e))

* Use PEP-380 to yield from the underlying generator ([`428f394`](https://github.com/abid-mujtaba/testing-fixtures/commit/428f394dff1165eb1a18b0ce751d2811f5e5c817))

* Rename definitions to fixture_factory ([`2470eb7`](https://github.com/abid-mujtaba/testing-fixtures/commit/2470eb7c4500cf02acc39b0c6796e3bccc4622e9))

* Make Fixture a reentrant and reusable context manager ([`76e7486`](https://github.com/abid-mujtaba/testing-fixtures/commit/76e7486538b758a3140b3747bb62258afe4e0daf))

* Add fixture_f and test which exposes the need for a reentrant fixture ([`804e91a`](https://github.com/abid-mujtaba/testing-fixtures/commit/804e91a6c82d84071dcaff051dcff7bac7b6ed81))

* Refactor Fixture implementation to match contextlib._GeneratorContextManager which necessitate using an alias for Generator instead of Iterator ([`7f531b3`](https://github.com/abid-mujtaba/testing-fixtures/commit/7f531b300ba1ed018ab43d08e1ca9acabd5575e5))

* Uncomment fixture_e (mutable state) and its test ([`d0b29a6`](https://github.com/abid-mujtaba/testing-fixtures/commit/d0b29a6087fc9447f6f934415422941c1f5234fd))

* Uncomment fixture_d and its associated tests ([`d72d113`](https://github.com/abid-mujtaba/testing-fixtures/commit/d72d113b50d20d49b11b77e82567220cb506c8a2))

* Define a compose parametrized decorator used to compose fixtures at the definition level ([`1580b99`](https://github.com/abid-mujtaba/testing-fixtures/commit/1580b994fe4ba51db0fec9572d1e9e57c08df5cc))

* Refactor implementation so that fixtures are both decorators and context managers ([`fb43adf`](https://github.com/abid-mujtaba/testing-fixtures/commit/fb43adfdea500317523642c12cb6f9dfaede2836))

* Comment out fixtures and tests that use fixture composition ([`53eff36`](https://github.com/abid-mujtaba/testing-fixtures/commit/53eff36a97412d66ca176b8f3b2947ca4739168b))

* Revert so that fixtures only apply to functions that return None (tests) ([`6450e0a`](https://github.com/abid-mujtaba/testing-fixtures/commit/6450e0a06f0d1e7c4a4a5e7f5a1807f1b4bd2581))

* Use wraps to get correct name of decorated fixture definition ([`3b82fd4`](https://github.com/abid-mujtaba/testing-fixtures/commit/3b82fd43a3ae4fe1e225b3f37331c8f0524f26f3))

* Refactor types and yields for fixtures e and f ([`e5ff2fb`](https://github.com/abid-mujtaba/testing-fixtures/commit/e5ff2fbebfb9b8eee7c3703e5c4601ea7081935d))

* Refactor types and yielded values up to fixture_d ([`5a1ab0d`](https://github.com/abid-mujtaba/testing-fixtures/commit/5a1ab0d1082e7da718d52226603d5b0102062297))

* Partial refactor away from strings to TypedDict showing injection cleanly ([`da149c8`](https://github.com/abid-mujtaba/testing-fixtures/commit/da149c8b646fd6800dc0b677d23c24f3b4cd3a7a))

* Ignore invalid-name pylint errors ([`0562c65`](https://github.com/abid-mujtaba/testing-fixtures/commit/0562c65d71b7a742ee963b1fbc34606979a7b85a))

* Skip the known failing test ([`5c31315`](https://github.com/abid-mujtaba/testing-fixtures/commit/5c313158bc121c3f704b060f23eb5d5f0676b232))

* Add example of double injected fixture that requires a re-entrant context manager ([`dfa57c1`](https://github.com/abid-mujtaba/testing-fixtures/commit/dfa57c1e9add13898a0987ddccb93856665a7335))

* Add example of multiple fixtures applies to a single test function ([`4dbbd7f`](https://github.com/abid-mujtaba/testing-fixtures/commit/4dbbd7f07767ee6acd30912875a8924573cdde36))

* Add example of fixture that takes injections from both another fixture and the test site ([`2f4c7e4`](https://github.com/abid-mujtaba/testing-fixtures/commit/2f4c7e407da1332fddea620ca0e308e6fd1b1fc3))

* Allow fixture to be applied to other fixtures ([`407b937`](https://github.com/abid-mujtaba/testing-fixtures/commit/407b9372446ac1329f37a1e38b396af50fc46517))

* Implement tunability of created fixtures ([`40d9cb4`](https://github.com/abid-mujtaba/testing-fixtures/commit/40d9cb4519a03fdadb788511564414fc940e7b0b))

* Add usage of a fixture parametrized from the test function decoration site ([`a33b826`](https://github.com/abid-mujtaba/testing-fixtures/commit/a33b826945ae691b4cb7bc22db942cda27d4b78b))

* Add types to the fixture tool ([`81e1cbf`](https://github.com/abid-mujtaba/testing-fixtures/commit/81e1cbf37ca0a3249ccf5ee49bf097993a9cb47d))

* Initial implementation of fixture creator (untyped) ([`fb009ec`](https://github.com/abid-mujtaba/testing-fixtures/commit/fb009ec1b06793963d731dcb6ba62c2b111deb78))

* Add example use case: decorated test, fixture definition ([`e9f2095`](https://github.com/abid-mujtaba/testing-fixtures/commit/e9f209529b7887bd3d9add5916266dfb83f77fc2))

* Refactor to inject yielded value as first argument which reduces nesting and allows for appropriate typing ([`20ae34b`](https://github.com/abid-mujtaba/testing-fixtures/commit/20ae34b68b61d9703682078c779c89a54dba1feb))

* First implementation of a 5 level deep tunable_fixture decorator for fixture generators ([`4c101da`](https://github.com/abid-mujtaba/testing-fixtures/commit/4c101da34ad21db424f6ce6baf23638844a003ce))

* Add README ([`8b98b19`](https://github.com/abid-mujtaba/testing-fixtures/commit/8b98b19324f1059cca83ca53d37e805cae89d8ca))

* Add remaining tests for operations including a missing one ([`f719d63`](https://github.com/abid-mujtaba/testing-fixtures/commit/f719d6307173b15948115b59c0462ee98fce5701))


## v0.0.1 (2022-10-30)

### Unknown

* Refactor to package the server using hatch ([`c798a2f`](https://github.com/abid-mujtaba/testing-fixtures/commit/c798a2f61befe65401e2bc457c2a51d1ce49b91c))

* Implement tunable fixture ([`953cbe3`](https://github.com/abid-mujtaba/testing-fixtures/commit/953cbe339c3cc749c044698ba1fd799ebdacf84d))

* Comment out uuid and operation fixture we won&#39;t be using any more ([`cb7ca69`](https://github.com/abid-mujtaba/testing-fixtures/commit/cb7ca6994a61c9c8ee1e878ddc62f3fcf1701cda))

* Add square and cube operations to processor ([`766c1f8`](https://github.com/abid-mujtaba/testing-fixtures/commit/766c1f81c448846de378c4716e11831968741713))

* Add fixture for injecting operation into DB before running test ([`5dbfa94`](https://github.com/abid-mujtaba/testing-fixtures/commit/5dbfa94da9b1a120628f096bb2dd24afa8ed12d3))

* Add logic for identity operations ([`3fdad50`](https://github.com/abid-mujtaba/testing-fixtures/commit/3fdad5043ea4ccb85900f2d6732fb25c3caa6ba4))

* Allow autocommit to ge configurable ([`f654a9f`](https://github.com/abid-mujtaba/testing-fixtures/commit/f654a9fbffa356fc0941785e3903a9b7f2a37a5c))

* Give tests access to the DB accessor for fixtures ([`6e580a3`](https://github.com/abid-mujtaba/testing-fixtures/commit/6e580a3fffd0f6170be5835be873c455d6b0b94d))

* Add postgres DB accessor ([`78fe36d`](https://github.com/abid-mujtaba/testing-fixtures/commit/78fe36dd3e1ff192af615abe239e328da0ca5272))

* Install psycopg (v3) into server and test containers ([`271ecb8`](https://github.com/abid-mujtaba/testing-fixtures/commit/271ecb884828029e154ade537d925a6818de3047))

* Modify compose config to inject db password via env var ([`fac3f92`](https://github.com/abid-mujtaba/testing-fixtures/commit/fac3f92cfda66ac7d472a81429e9b605bf096413))

* Add postgres container and initiate operations table ([`d5dfef2`](https://github.com/abid-mujtaba/testing-fixtures/commit/d5dfef2188db4ca046ecf7b24f7cfcb9b8f78f90))

* Add incomplete handler for /compute end-point (parses request payload) ([`2194661`](https://github.com/abid-mujtaba/testing-fixtures/commit/219466128accc75766e48885b350bc58259a7ef2))

* Add healtcheck (netcat) to server ([`1cb8b54`](https://github.com/abid-mujtaba/testing-fixtures/commit/1cb8b54c5f6318c0cb1f1acddedf6fafa06769cb))

* Add failing first test for /compute end-point ([`a60ee5e`](https://github.com/abid-mujtaba/testing-fixtures/commit/a60ee5e6ac79273fb754b94fe9c50e5c5206be4e))

* Refactor base_url into a fixture ([`9843c58`](https://github.com/abid-mujtaba/testing-fixtures/commit/9843c58af90e2cb70d489c3439394a3485267376))

* Fix pylint and mypy errors ([`f7f58fe`](https://github.com/abid-mujtaba/testing-fixtures/commit/f7f58fec1815d06b49eb2e77a51950ea1f1f0616))

* Add simple test for /test end-point ([`2d34dac`](https://github.com/abid-mujtaba/testing-fixtures/commit/2d34dace702e3ea4e14a05b71d6a83dc690e02e6))

* Implement flask server with just /test end-point ([`aac3f33`](https://github.com/abid-mujtaba/testing-fixtures/commit/aac3f33358f6355febc1fd5892203db26215efcb))

* Add docker config for server and test client ([`2918f99`](https://github.com/abid-mujtaba/testing-fixtures/commit/2918f99698c9cb84023ebf9a516ed80747a3397c))

* Initial commit (empty .gitignore) ([`83b1a7b`](https://github.com/abid-mujtaba/testing-fixtures/commit/83b1a7beb2ac837f8a75d4a34ab2c100a454d2a8))
