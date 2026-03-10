Build a small, useful CLI tool or utility that can be published to npm/PyPI for downloads and potential sponsorship.

## Step 1: Find an unmet need
Use WebSearch to research:
- "most wanted CLI tools 2026"
- "python utility scripts people need"
- "npm packages with few stars but many downloads"
- "github trending repositories CLI tools"
- "reddit r/commandline what tool do you wish existed"

## Step 2: Evaluate ideas
Pick a tool that:
- Solves a real pain point developers have
- Can be built in a single session (< 500 lines)
- Doesn't already exist (or existing solutions are bad)
- Has a catchy name
- Is easy to install and use

## Step 3: Build it
- Create project in /Users/corri/tools/<tool-name>/
- Write clean, well-documented code
- Include a good README.md
- Add a LICENSE (MIT)
- Include package.json or setup.py for easy installation
- Write basic tests

## Step 4: Publish
- If npm credentials exist: `npm publish`
- If PyPI credentials exist: `pip install twine && python setup.py sdist && twine upload dist/*`
- Push to GitHub for visibility

## Step 5: Track
Update memory/tools.md with:
- Tool name, description, repo URL
- Download counts if available
- Ideas for improvements

## Tool ideas that tend to do well:
- Developer productivity tools (git helpers, file organizers)
- Data format converters (JSON<->CSV, YAML<->JSON)
- API testing/mocking utilities
- Log analyzers and formatters
- Markdown tools (table generators, link checkers)
- dotfile managers
