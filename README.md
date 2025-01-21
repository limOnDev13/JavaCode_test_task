# JavaCode test task
A test assignment from the JavaCode company.

## Description
A web application that allows you to manage wallets - change the balance and get the current balance. The special feature of the application is the ability to keep a high load, thanks to load balancing using nginx and 4 running instances of the application with 4 workers in separate containers, asynchronous request processing using FastAPI, a cache with a backend on Redis and asynchronous work with the Postgres database.

## Demo

To demonstrate the API, the Postman collection has been added to the repository. Stress tests (asynchronous and on threads) have been added to demonstrate the ability to withstand heavy loads. You can run them with the application running or view the results in the /stress_tests/results folder.

---
## Setup and launch

To launch the application, it is enough to download the project to the machine (you don't have to download the files in the tests, stress_tests, files requirements-dev.txt , setup.cfg), set environment variables as shown in the example .env.example and assemble docker containers (using the ```docker compose up --build``` command from the project root). If errors occur during startup (most likely related to the creation of the table), restart the containers. **WARNING!** The number of application instances in docker-compose.yml and the number of workers depend on the number of logical cores on the machine. My machine has 16 logical cores, and 4 instances of the application on 4 workers are just right for 16 cores. When setting up a project on your machine, keep this fact in mind. If the total number of workers is higher or lower than the number of logical processors, the application may lose performance.

If the application is running on a local machine, requests can be sent to http://localhost:8080.
If you need to change some files in containers, it is enough to add volumes to applications. **WARNING!** You need to add a separate volume for each container so that there are no conflicts (for example, in log files).
___

## Endpoints

- **GET /api/v1/wallets/{wallet_uuid}** - Get a wallet balance
- **POST /api/v1/wallets/{wallet_uuid}/operation** - Update the wallet balance

For more detailed documentation, you can use Swagger (http://localhost:8080/docs )
___

## Technologies
- FastAPI
- Postgres
- SQLAlchemy
- Redis
- Docker
- Nginx
- Swagger
- Postman
- pytest

## Ways of development and improvement

- At the moment, the application reads environment variables from the .env file in an unordered manner. It is planned to add a function that will read the .env file in a separate stream. If volumes are added to applications, this will allow you to make changes to the environment variables (and, accordingly, the application configuration) without restarting the containers.
- Perhaps it is possible to increase the resilience of the application to high loads by using a task queue on Celery. I don't know this technology yet, but once I get the hang of it, I might be able to add it to the project.
