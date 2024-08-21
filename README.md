# spotify-bpm-checker

Checks a playlist's tracks for their BPM (beats per minute).

## Setup guide

1. Clone the repository, and go to the root directory of the project.
2. Create a virtual environment:

```bash
python -m venv .venv # or use specific version of python, e.g. python3.12
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate # or .venv/Scripts/activate on Windows
```

4. Install `poetry` with pip:

```bash
pip install poetry
```

5. Go to the `app` directory and install dependencies with poetry:

```bash
cd app
poetry install
```

6. Create a .env file in the root directory and add the following:

```bash
CLIENT_ID=<ask Marcus>
CLIENT_SECRET=<ask Marcus>
```

## Usage

```bash
cd app # If not already in the app directory
export PYTHONPATH=.
python <python_file_to_run>

# e.g.
python src/bpm_feature.py
```
