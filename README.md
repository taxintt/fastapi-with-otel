# what's this?
This is the FastAPI-based application that uses OpenTelmetry.

- poetry
- pytest (w/ pytest-cov)
- tox
- pre-commit

## Run local app
```bash
make local
```

## Deploy to Cloud run
```bash
make deploy PROJECT=${gcp_project_id}
```