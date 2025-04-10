# Berkeley Course Recommender

## Installation

Requires Python>=3.11. Check out Pyenv or Miniconda for installing python versions.

MacOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate

cd app
pip install -r requirements-dev.txt

cd search
pip install -e .
```

## Development

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files # if you want to test it manually
```

### Local Deployment

In the search directory
```bash
uvicorn src.main:app --reload
```

Then go to /docs
