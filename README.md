# Accelerator I: Enterprise Days — Python Track

This is a monorepo containing multiple projects for the Accelerator Program Year One Enterprise Days for Python developers.

Each project in this monorepo is considered separate. The only shared files are:

- dev-requirements.txt
- .flake8
- .pre-commit-config.yaml
- pyproject.toml

Each project must have its own:

- requirements.txt
- .mypy.ini
- other project related files

## Getting started

Commands to run after cloning this repo:

- `pre-commit install`

### Recipe store

The recipe store is responsible for maintaining recipes and ingredients.
It exposes a REST API, for which the definition can be found at `/api/schema/`
(see `recipe_store.urls` for other endpoints with schema information).

#### Start the recipe store

Run all of these commands inside the `recipe_store` project.

1. Copy `.env.sample` to `.env` and set the correct values
2. Create a Postgres database called `recipe_store`
3. Run `python manage.py migrate`
4. Run `python manage.py createsuperuser`
5. Run `python manage.py runserver`

This should expose the recipe store API at http://localhost:8000

#### Type checking

This project uses mypy for type checking, which isn't run automatically by pre-commit.
So run `mypy .` inside the `recipe_store` project to do type checking.
