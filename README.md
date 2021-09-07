# Monitoring - DISI Industrial Workshop @ UniTN

This repository contains the demo presented in the DISI Industrial Workshop at the University of Trento on 23. November 2023.

## Introduction

Monitoring is the art of knowing, precisely and in real-time if a system is running correctly in production.
A well-implemented monitoring solution allows us to detect anomalies automatically, find problems before they affect the users, and find the root cause of performance issues, outages, and disruptions.
Monitoring helps developers and operations people to improve the software and run it successfully in production.

This workshop will cover the main monitoring concepts with concrete examples from real-life problems.
We will instrument and monitor a simple web application step-by-step using the great open-source tools Prometheus and Grafana.
At the end of the presentation, you will have a good understanding of the basics of monitoring and be able to use it for projects.

For practical reasons, coding will be done on the presenter's screen.
This repository contains all the code presented during the workshop.
The `master` branch contains the starting code.
You can find the solution in the `solution` branch.

## Disclaimer ⚠️

The setup and the code in this demo are **NOT** production-ready and contain serious security problems (missing authentication, too broad privileges, etc.).
**Use it at your own risk!**
The demo aims to illustrate concepts, patterns, and tools to implement monitoring in real-world applications.

## Structure

The repository uses Docker Compose to run all the different needed components.
Each component is in its directory at the top level and includes a Dockerfile, the required configuration, and, sometimes, code.
While it is possible to build and run each component independently, the best way to run the demo is to use Docker Compose.

### Docker Compose

#### Start

Use the following command to start the demo:

```sh
docker-compose build
docker-compose up
```

#### Stop

Use the following command to stop the demo:

```sh
docker-compose stop
docker-compose rm --force
```

### Components

#### Frontend

We have prepared a straightforward Todos application: you can create, modify, mark as done, and delete Todos.
The application is written in [React](https://reactjs.org/) and uses the CSS from [TodoMVC](http://todomvc.com/)
Don't worry: you will not need to read or modify the source code 😉.

The frontend will be running on port [8000](http://localhost:8000).

#### Backend

We will store our impressive Todo list on a backend.
The backend is simple.
It is written in Python 3 and uses [FastAPI](https://fastapi.tiangolo.com/) to expose REST APIs and PostgreSQL to store the data.
**You will need to modify the backend code to add some metrics with Prometheus**.
For more details, please check out the [backend](./backend) folder.

The backend will expose the REST APIs on port [5000](http://localhost:5000) and the Prometheus metrics on port [5001](http://localhost:5001).

#### PostgreSQL

You know that already: we will use the fantastic [PostgreSQL](https://www.postgresql.org/) to store our Todos.

#### Bot

A simple Python bot 🤖 generates some load on the backend to collect decent metrics.
The code is straightforward, but you don't have to read or understand it.

#### Grafana

[Grafana](https://grafana.com/) is an analytics platform that allows you to query, visualize, alert, and understand your metrics.
It enables developers to create, explore, and share dashboards with plots and visualizations of data stored in many sources.
We will use it to visualize the collected metrics in dashboards.
The Docker container already contains them.

It will be running on port [3000](http://localhost:3000).

#### Prometheus

[Prometheus](https://prometheus.io/) is an open-source system monitoring and alerting toolkit originally built at SoundCloud.

It has two main components:

- Prometheus server, which scrapes and stores time-series data
- Client libraries for instrumenting application code

We will use both components:

- We will instrument the [backend](./backend) code with the [Prometheus Python client](https://github.com/prometheus/client_python).
- We will use the server to collect the metrics and serve them to Grafana.

Similar to Grafana, the Prometheus server is already configured for you.

We won't need it, but the UI will run on port [9090](http://localhost:9090).

## License

This repository contains free software released under the MIT Licence.
Please check out the [LICENSE](LICENSE) file for details.
