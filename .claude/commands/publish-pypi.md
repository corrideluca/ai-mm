Publish a package to PyPI registry.

Steps:
1. Activate venv if needed
2. Install build tools: `pip install build twine`
3. Build the package: `python -m build`
4. Check if PyPI token exists in ~/.pypirc
5. If not, tell user to create API token at https://pypi.org/manage/account/token/
6. Upload: `python -m twine upload dist/*`
7. Verify: `pip install <package-name>` from PyPI
8. Update memory/content.md
9. Tweet about the PyPI launch
