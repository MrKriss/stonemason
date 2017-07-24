
from pathlib import Path
import pytest
import git
import json

from conftest import TEST_DIR


def test_init_with_project(tmpdir):

    output_path = Path(tmpdir.strpath)

    # Set arguments
    args = f"init -o {output_path.as_posix()} {TEST_DIR}/data/python-project"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    # Check files were created
    package_name = 'testpackage'
    files = [
        '.git/',
        '.mason',
        'MANIFEST.in',
        'README',
        'requirements.txt',
        'setup.py',
        'src/testpackage',
        'src/testpackage/__init__.py',
        'src/testpackage/main.py'
    ]
    for f in files:
        p = output_path / package_name / f
        assert p.exists()

    # Check requirements were polulated
    target = "requests\nlogzero\n"
    req_file = output_path / package_name / 'requirements.txt'
    text = req_file.read_text()
    assert text == target

    # Check git repo was created and commits made
    repo_dir = output_path / package_name
    r = git.Repo(repo_dir.as_posix())
    log = r.git.log(pretty='oneline').split('\n')
    assert len(log) == 1
    assert "Add 'package' template layer via stone mason." in log[0]


def test_init_with_project_and_template(tmpdir, no_prompts):

    output_path = Path(tmpdir.strpath)

    # Set arguments
    args = f"init -o {output_path.as_posix()} {TEST_DIR}/data/python-project/pytest"

    from stonemason import main
    # Run from entry point
    main.main(args=args)

    # Check files were created
    package_name = 'testpackage'
    files = [
        '.git/',
        '.mason',
        'MANIFEST.in',
        'README',
        'requirements.txt',
        'setup.py',
        'src/testpackage',
        'src/testpackage/__init__.py',
        'src/testpackage/main.py',
        'tests/test_foo.py'
    ]
    for f in files:
        p = output_path / package_name / f
        assert p.exists()

    # Check requirements were polulated
    target = "requests\nlogzero\npytest\npytest-cov\ncoverage\n"
    req_file = output_path / package_name / 'requirements.txt'
    text = req_file.read_text()

    assert text == target

    # Check git repo was created and commits made
    repo_dir = output_path / package_name
    r = git.Repo(repo_dir.as_posix())
    log = r.git.log(pretty='oneline').split('\n')
    assert len(log) == 2
    assert "Add 'pytest' template layer via stone mason." in log[0]
    assert "Add 'package' template layer via stone mason." in log[1]