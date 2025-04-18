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

Make a copy of `.env.example` as your `.env` file and fill in the relevant sections.

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files # if you want to test it manually
```

### Local Deployment

In the search directory
```bash
uvicorn src.search.main:app --reload
```

Then go to /docs
