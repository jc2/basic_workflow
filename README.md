# Basic Workflow
This projects is a demo. The idea is to simulate a workflow with different Bank transactions (consult, deposit, withdraw). The flow is described in a JSON file. Take a look to the file: `example.json`

- [Basic Workflow](#basic-workflow)
- [Todo](#todo)
- [How to RUN using docker compose](#how-to-run-using-docker-compose)
- [Users](#users)
  - [Create user](#create-user)
  - [Get users](#get-users)
- [Load Workflow](#load-workflow)
- [How to test](#how-to-test)

# Todo
- [ ] Unittest as classe
- [ ] Add functional tests
- [ ] Add fixtures
- [ ] Improve Custom Exceptions
- [ ] Add dotenv
- [ ] Add factory for tests to create things in DB and delete them at the end
- [ ] Session security
- [ ] Api Logs
- [ ] Add Tox
- [ ] Add Black
- [ ] Add a Docker entry point
- [ ] Add extensions such as Mongo as factories
- [ ] Add a seed function to pre-populated db
- [ ] Create a app to manage users

# How to RUN using docker compose
This project use an external API to convert currencies. You need to create an account in currencyconverterapi.com and set the APIKEY in the `.env` file
- Create a file using `./config/mongo/mongo-init.js.example` as template. Keep the same name
- Create a file using `.env.example` as template. Keep the same name
- `docker-compose up --build`
- Go to: `localhost:8000/users/`

# Users
## Create user
- `curl --header "Content-Type: application/json" --request POST --data '{"user_id":"105398891","pin":2090, "balance": 1000000}' http://localhost:8000/users/`
## Get users
- `curl http://localhost:8000/users/`

# Load Workflow

# How to test
- `pip install -r requirements.txt`
- Export env var in the `.env` file
- `pytest -v`