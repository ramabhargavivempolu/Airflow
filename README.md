# Airflow

This repository contains a local Apache Airflow setup powered by Docker Compose.

## Push this code to GitHub

The repo already points to:

`https://github.com/ramabhargavivempolu/Airflow.git`

Use the normal git flow:

```bash
git add .
git commit -m "Add Airflow DAG and CI workflow"
git push origin main
```

## Traditional CI/CD for this repo

### CI

GitHub Actions runs on every push to `main` and every pull request to `main`.

It currently:

- installs the project dependencies
- checks Python syntax in `dags/`
- validates that Airflow can import the DAGs

Workflow file:

`.github/workflows/ci.yml`

### CD

For Airflow, "traditional CD" usually means deploying the `dags/` folder to a running Airflow environment after CI passes.

Typical production options:

1. GitHub Actions copies DAGs to a VM using SSH/rsync.
2. GitHub Actions builds and pushes a custom Airflow Docker image.
3. GitHub Actions deploys to a managed Airflow service such as MWAA, Composer, or Astronomer.

This repo is ready for CI now. The CD step depends on where you want your Airflow instance to run.
