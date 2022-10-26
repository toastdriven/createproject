# `createproject`

For creating new Python packages.

I just used to cargo-cult this stuff around anyway. Let's make it better.


## Install

* `git clone ...`
* `cd ...`
* `virtualenv env`
* `. env/bin/activate.fish`
* `pip install -r requirements.txt`
* `cp .env-dist .env` (and customize)


## Usage

* `./bin/create_project.py`

Then follow the prompts.


## Example

```bash
(env) $ ./bin/create_project.py
Package name? squeal
Version? [0.1.0]
Description? [] A query library for generating SQL

Your full name? [Daniel Lindsley]
Your email? [daniel@toastdriven.com]
Your GitHub username? [toastdriven]

Code root directory? [/Users/daniel/Code]
Initialize Git? [Y/n]
Initialized empty Git repository in /Users/daniel/Code/squeal/.git/

Created Python package '/Users/daniel/Code/squeal'.
```


## License

New BSD
