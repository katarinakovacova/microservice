# microservice 

Product aggregator microservice. It is REST API Python microservice which allows users to browse a product catalogue and which automatically updates prices from the offer service, provided by Applifting. 

## Usage

This microservice is containerized. You will need Docker to run this app. To run this app please create `.env` file which has the following template:

```env
POSTGRES_PASSWORD="xxxxx"
REFRESH_TOKEN="xxxxx"
OFFERS_BASE_URL="https://python.exercise.applifting.cz"
AUTH_USERNAME="you"
AUTH_PASSWORD="areNumber1"
```

Then type the following command: 

```bash
docker compose up --build
```

## Documentation

Once the app is running, you can obtained Swagger documentation at `/docs` endpoint. 
