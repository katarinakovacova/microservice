# Microservice 

## Overview

The Product Aggregator Microservice is a REST API built with Python that enables users to browse a dynamic product catalogue. This microservice automatically updates product prices by fetching data from the offer service provided by Applifting. It is designed for scalability and efficiency, allowing seamless integration with various frontend applications.

## Features

- **Product Catalogue Browsing**: Users can easily navigate through a wide range of products.
- **Automatic Price Updates**: Prices are updated in real-time from the offer service, ensuring users have access to the latest information.
- **User Authentication**: Secure access to the microservice is facilitated through authentication mechanisms.
- **Containerized Environment**: The microservice is packaged in Docker containers for easy deployment and scalability.
- 
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

## Contact

For any questions or support, please contact [Katarína Kováčová](mailto:katarinakovacova100@gmail.com).
