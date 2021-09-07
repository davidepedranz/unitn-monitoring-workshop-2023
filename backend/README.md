# Todos Backend

Welcome to our super sophisticated Todos app 😎.

The backend is an easy [FastAPI](https://fastapi.tiangolo.com/) application that allows creating, reading, updating, and deleting Todos.

The application works fine, but the performance is not fantastic: some bugs are making the system slow.

Your goal is to find the bugs 🐛🐞🦗 and fix them 🧐.
You will instrument the code to export metrics to [Prometheus](https://prometheus.io/) and use [Grafana](https://grafana.com/) to create beautiful dashboards 🤩.

Are you ready for the challenge? 💪🏻💪🏻💪🏻

## Setup

This project is built in Python 3 and uses [Poetry](https://python-poetry.org/) to manage dependencies.
Make sure you have Python 3.11 and Poetry installed.

Install the dependencies as follows:

```shell
poetry install
```

The application requires a working PostgreSQL database.
Please follow the instructions in the [top-level README](../README.md) to run it using Docker Compose.

Run the [main.py](app/main.py) from PyCharm.
If you prefer the command line, you can use the following command:

```shell
poetry shell
PYTHONPATH=. python ./app/main.py
```

## Task

Measure the execution time of the different database operations.

Please name the metric `app_repository_query_duration_seconds` with the label `query` to take advantage of the existing [Grafana dashboards](http://localhost:3000).

The solution requires only a few lines of code to the [InstrumentedRepository](app/core/database/repository/instrumented.py) class.
Please refer to the slides for code snippets or check out the official documentation of the [Prometheus Python client](https://github.com/prometheus/client_python).

## Solution

The solution is available in the `solution` branch in git.
