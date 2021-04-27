# Basic Workflow
This projects is only a demo. 

# Todo
- [ ] Unittest as classes
- [ ] Add functional tests
- [ ] Add factory for tests
- [ ] Session security
- [ ] Api Logs
- [ ] Add Tox
- [ ] Add Black
- [ ] Add a Docker entry point

# How to RUN using docker compose
- Create a file using `./config/mongo/mongo-init.js.example` as template. Keep the same name
- Create a file using `.env.example` as template. Keep the same name
- `docker-compose up --build`
- Go to: `localhost:8000/users/`

# Users
## Create user
- `curl --header "Content-Type: application/json" --request POST --data '{"name":"jc","email":"jc@m.com"}' http://localhost:8000/users/`
## Get users
- `curl http://localhost:8000/users/`

# Load Workflow

# How to test
- `pip install -r requirements.txt`
- `pytest -v`