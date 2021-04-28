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
- [ ] Unittest as classes
- [ ] Add functional tests
- [ ] Add fixtures
- [ ] Add dotenv
- [ ] Add factory for tests
- [ ] Session security
- [ ] Api Logs
- [ ] Add Tox
- [ ] Add Black
- [ ] Add a Docker entry point

# How to RUN using docker compose
This project use an external API to convert currencies. You need to create an account in currencyconverterapi.com and set the APIKEY in the `.env` file
- Create a file using `./config/mongo/mongo-init.js.example` as template. Keep the same name
- Create a file using `.env.example` as template. Keep the same name
- `docker-compose up --build`
- Go to: `localhost:8000/users/`

# Users
## Create user
- `curl --header "Content-Type: application/json" --request POST --data '{"user_id":"jc","pin":12345}' http://localhost:8000/users/`
## Get users
- `curl http://localhost:8000/users/`

# Load Workflow

# How to test
- `pip install -r requirements.txt`
- `pytest -v`