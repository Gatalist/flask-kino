### Run locally:
Run in terminal:
`docker compose -f docker-compose.yml up --build`  

### migrations:
Run in terminal:
`docker exec -it flask_app /bin/bash`
`flask db init`
`flask db migrate`
`flask db upgrade`

