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

## Installation

```console
pip install co-mit
```

## Usage

```console
cmt --help
```

1. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
2. Navigate to the root of your git repository.
3. Run `cmt` or `co-mit` to generate a commit message.

## License

`co-mit` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Development

I will assume you have [uv](https://docs.astral.sh/uv/) installed.

To install `co-mit` along with the tools you need to develop and run tests, run the following in your uv virtualenv:

```console
uv pip install -e .[dev]
```
