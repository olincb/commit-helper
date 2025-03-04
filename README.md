# co_mit
helps with commits!

[![PyPI - Version](https://img.shields.io/pypi/v/co-mit.svg)](https://pypi.org/project/co-mit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/co-mit.svg)](https://pypi.org/project/co-mit)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Development](#development)
    - [Running co_mit](#running-co_mit)
    - [Publishing](#publishing)

## Installation

```console
pip install co-mit
```

## Usage

```console
 » co-mit --help

 Usage: co-mit [OPTIONS]

 Helps with git commits.

╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --openai-key  -k  TEXT  OpenAI API key. Can also set with OPENAI_API_KEY    │
│                         environment variable.                               │
│ --example     -e  TEXT  Example input to generate a commit message from.    │
│ --quiet       -q        Suppress all output other than final commit         │
│                         message. Useful for scripting. Can also set with    │
│                         CO_MIT_QUIET environment variable.                  │
│ --help                  Show this message and exit.                         │
╰─────────────────────────────────────────────────────────────────────────────╯
```

1. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
2. Navigate to the root of your git repository.
3. Run `cmt` or `co-mit` to generate a commit message:

```console
$ co-mit
Generating commit message...
running `git status`
running `git diff`
feat(cli): add `--example` option for generating commit messages

- Introduce the `--example (-e)` option to allow users to provide example
input for commit message generation.
- Update the CLI to handle the `--example` parameter and pass it to the
commit flow.
- Enhance the `CommitFlow` to incorporate example-based formatting
instructions.
- Improve the README with detailed usage instructions and examples, including
the new `--example` option.
```

## License

`co-mit` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Development

I will assume you have [uv](https://docs.astral.sh/uv/) installed.

To install `co-mit` along with the tools you need to develop and run tests, run the following in your uv virtualenv:

```console
uv pip install -e .[dev]
```

### Running co_mit

After installing the package, you can run the CLI with:

```console
co-mit
```

To run with dotenv file:

```console
dotenv run -- co-mit
```

### Publishing

To publish a new version to PyPI, update the version number with hatch:

```console
hatch version minor
# or major, patch, etc.
```

Then push a tag or create a new release on GitHub.

A GitHub Actions workflow will automatically publish the new version to PyPI
when a new tag is pushed to the repository, or a new release is created.
