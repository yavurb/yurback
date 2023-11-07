# Yurback

A backend built with python to serve information to [yurb.dev](https://yurb.dev)

This backend is also the core hearth for all the features of **yurb.dev** and a proxy-like backend for future projects.

#### OpenAPI Docs

You can see a detailed documentations about the APIs available [here](https://api.yurb.dev/docs)

## ⚙️ Set up

_Yurback_ uses [PDM](https://pdm-project.org/latest/) to manage its dependencies. Use the following command to install all the projects's dependencies without altering the _lock_ file.

```sh
pdm sync
```

### Environment Variables 😶

_Yurback_ needs certain env variables to be able to run. In order to run the project locally, define all the env variables needed based on the `.env.template` file into a new `.env` file. Below is an example.

```py
PORT=1234
ENVIRONMENT="dev" # accepts dev | prod
JWT_SECRET="my-super-confidencial-secret"

# DB
DATABASE_URI="postgresql://{user}:{password}@{host}/{database}"

...
```

> It is worth noting that certain env variables such as `AWS_*` are not needed in production since the backend is built to run in AWS using IAM Roles. This allows the project to access all the AWS services required to work seamlessly.


## 🧞 Commands

All commands are run from the root of the project, from a terminal and using [PDM](https://pdm-project.org/latest/):

| Command                   | Arguments       | Action                                           | Examples                 	|
| :------------------------ | :-------------- | :----------------------------------------------- | :-------------------------	|
| `pdm sync`             		| 								| Installs dependencies                            |														|
| `pdm run dev`             | `--port`				| Starts local dev server at `localhost:8910`      | `pdm run dev --port 8080`	|
| `pdm run tests`           | 								| Run all tests using pytest											 |														|
| `pdm run tests_cov`       | 								| Run all tests and generate a coverage report     |														|
| `pdm run start`       		| 								| Starts prod-like server at `localhost:8910`			 |														|
| `pdm run db_revision` 		| 								| Create a new alembic revision                    |														|
| `pdm run db_upgrade` 		  | 								| Upgrade the DB to the latest revision            |														|
| `pdm run db_downgrade`	  | 								| Downgrade the DB to the previous revision        |														|

### Running installed packages

_PDM_ allows running installed packages through the `run` command. This means that every installed package, especially dev-related packages such as pytest, can be run without activating the virtual environment.

```sh
# Generates a report based on the latest test run
pdm run coverage report -m
```


## Technology Stack

This projects is built using [Python v3.11.x] or later. and uses the following stack.

- [PDM](https://pdm-project.org/latest/) - For package and dependency management.
- [FastAPI](https://fastapi.tiangolo.com/) - For web server provisioning.
- [Pydantic](https://docs.pydantic.dev/latest/) - For IO validation
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/index.html) - For models, querying and connection management.
- [PostgreSQL](https://www.postgresql.org/) - For SQL engine.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - For migrations management.
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - For AWS integration.
- [Pytest](https://docs.pytest.org/en/7.4.x/contents.html) - For unit testing.
- [Redocly](https://redocly.com/) - For OpenAPI documentation.
- [Docker](https://www.docker.com/) - For containerization.
