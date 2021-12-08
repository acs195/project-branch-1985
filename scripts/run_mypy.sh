#/bin/bash
# This is the script to run mypy linting
find . -name '*.py' ! -iname "test_*" ! -iname "conftest.py" \
    -not -path "./.vscode/*" \
    -exec mypy {} \;

exit 0
