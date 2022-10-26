#!/usr/bin/env python
import datetime
from pathlib import Path
import subprocess

from environs import Env


BASE_DIR = Path(__file__).parent.parent


# If this is ever the default value, you deserve to have your code break.
UNDEFINED_SENTINEL = "My Very Educated Mother Just Made Us Nine Pizzas"


def yes_or_no(msg, default=False):
    default_prompt = "y/N"

    if default is True:
        default_prompt = "Y/n"
    elif default is None:
        default_prompt = "y/n"

    answer = prompt(msg, default=default_prompt)
    answer = answer.lower()

    if "/" in answer and default is None:
        # They have to provide an answer.
        return yes_or_no(msg, default=default)

    if not answer:
        if default is None:
            # They have to provide an answer.
            return yes_or_no(msg, default=default)

        return default

    if (not answer.startswith("y")) and (not answer.startswith("n")):
        return yes_or_no(msg, default=default)

    return answer.startswith("y")


def prompt(msg, default=UNDEFINED_SENTINEL):
    msg = f"{msg}? "

    if default is not UNDEFINED_SENTINEL:
        msg = f"{msg}[{default}] "

    answer = input(msg)
    answer = answer.strip()

    if not answer:
        if default is UNDEFINED_SENTINEL:
            # They have to provide an answer.
            return prompt(msg, default=default)

        return default

    return answer


def get_template(template_name):
    template_dir = BASE_DIR / "templates"
    full_path = template_dir / template_name

    with open(full_path, "r") as in_file:
        return in_file.read()


def render(template, context):
    return template.format(**context)


def render_to_file(desired_path, template_name, context):
    template = get_template(template_name)
    output = render(template, context)
    out_path = desired_path

    with open(out_path, "w") as out_file:
        out_file.write(output)


def create_package_directories(code_root, package_name):
    desired_path = code_root / package_name

    if desired_path.exists():
        raise IOError(f"{desired_path} already exists!")

    desired_path.mkdir(parents=True)

    src_dir = desired_path / "src" / package_name
    src_dir.mkdir(parents=True)

    tests_dir = desired_path / "tests"
    tests_dir.mkdir(parents=True)


def create_gitignore(package_root, context):
    template_name = ".gitignore.tmpl"
    desired_path = package_root / ".gitignore"
    return render_to_file(desired_path, template_name, context=context)


def create_authors(package_root, context):
    template_name = "AUTHORS.tmpl"
    desired_path = package_root / "AUTHORS"
    return render_to_file(desired_path, template_name, context=context)


def create_justfile(package_root, context):
    template_name = "justfile.tmpl"
    desired_path = package_root / "justfile"
    return render_to_file(desired_path, template_name, context=context)


def create_license(package_root, context):
    template_name = "LICENSE.tmpl"
    desired_path = package_root / "LICENSE"
    return render_to_file(desired_path, template_name, context=context)


def create_manifest(package_root, context):
    template_name = "MANIFEST.in.tmpl"
    desired_path = package_root / "MANIFEST.in"
    return render_to_file(desired_path, template_name, context=context)


def create_pyproject(package_root, context):
    template_name = "pyproject.toml.tmpl"
    desired_path = package_root / "pyproject.toml"
    return render_to_file(desired_path, template_name, context=context)


def create_readme(package_root, context):
    template_name = "README.md.tmpl"
    desired_path = package_root / "README.md"
    return render_to_file(desired_path, template_name, context=context)


def create_setup(package_root, context):
    template_name = "setup.cfg.tmpl"
    desired_path = package_root / "setup.cfg"
    return render_to_file(desired_path, template_name, context=context)


def create_inits(package_root, context):
    src_init = package_root / "src" / context["PACKAGE_NAME"] / "__init__.py"
    src_init.touch(exist_ok=True)

    tests_init = package_root / "tests" / "__init__.py"
    tests_init.touch(exist_ok=True)


def run_git_init(package_root):
    subprocess.run(
        f"git init {package_root.as_posix()}",
        stderr=subprocess.PIPE,
        shell=True,
        check=True,
    )


def main(env):
    package_name = prompt("Package name")
    package_version = prompt("Version", default="0.1.0")
    description = prompt("Description", default="")
    print()
    full_name = prompt("Your full name", default=env.str("FULL_NAME", ""))
    email = prompt("Your email", default=env.str("EMAIL", ""))
    gh_username = prompt("Your GitHub username", default=env.str("GH_USERNAME", ""))
    print()
    code_root = prompt(
        "Code root directory", default=env.str("CODE_ROOT", BASE_DIR.parent)
    )

    package_path = Path(code_root) / package_name
    context = {
        "PACKAGE_NAME": package_name,
        "PACKAGE_VERSION": package_version,
        "FULL_NAME": full_name,
        "EMAIL": email,
        "GH_USERNAME": gh_username,
        "CODE_ROOT": code_root,
        "DESCRIPTION": description,
        "YEAR": datetime.date.today().year,
    }

    create_package_directories(Path(code_root), package_name)
    create_gitignore(package_path, context)
    create_authors(package_path, context)
    create_justfile(package_path, context)
    create_license(package_path, context)
    create_manifest(package_path, context)
    create_pyproject(package_path, context)
    create_readme(package_path, context)
    create_setup(package_path, context)
    create_inits(package_path, context)

    if yes_or_no("Initialize Git", default=True):
        run_git_init(package_path)

    print()
    print(f"Created Python package '{package_path.as_posix()}'.")


if __name__ == "__main__":
    env = Env()
    env.read_env()

    main(env)
