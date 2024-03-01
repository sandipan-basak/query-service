# FastAPI Query Handler Application

## Overview

This application provides an API for handling queries by converting them into embeddings, searching for the most relevant documents using FAISS, optionally caching responses with Redis, and generating responses based on the documents' metadata. It's built with FastAPI and is designed to be containerized with Docker.

## Prerequisites

- Docker
- An `.env` file configured with necessary API keys and paths.

## Configuration

Before running the application, create an `.env` file in the project root with the following contents:

```env
COHERE_API_KEY=<your-cohere-api-key>
FAISS_INDEX_PATH=/usr/src/app/data/indices/combined_index.index
FAISS_METADATA_PATH=/usr/src/app/data/indices/metadata.json
REDIS_URL=redis://redis:6379
OPEN_API_KEY=<your-open-api-key>
```
This file includes the necessary configurations for external services and paths to data indices.

## Building the Docker Image

To build the Docker image for this application, navigate to the root directory of the project and run:

```sh
docker build -t fastapi-query-handler .
```

This command builds a Docker image named fastapi-query-handler based on the provided Dockerfile.

## Running the Application

After building the image, you can run the application with Docker using the following command:

```sh
docker run -d --name my-fastapi-app -p 80:80 fastapi-query-handler
```

This command runs the application in a detached mode, maps port 80 of the container to port 80 on the host, and names the container my-fastapi-app.

## API Usage

Once the application is running, you can send queries to the /query endpoint using a tool like curl or Postman. Here is an example using curl:

```sh
curl -X 'POST' \
  'http://localhost/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "queries": ["<your query here>"]
}'
```

Replace "<your query here>" with your actual query.

## Development

For development purposes, the application can be run inside a Docker container to ensure consistency across different environments. This approach uses the Dockerfile provided to build and run the application, simulating a production environment on your local machine.

First, build the Docker image with the following command:

```sh
docker build -t fastapi-query-handler .
```

To run the application in development mode with live reloading, you can use the following command:

```sh
docker run -d --name fastapi-dev -p 80:80 -v $(pwd):/usr/src/app fastapi-query-handler uvicorn src.main:app --reload --host 0.0.0.0 --port 80
```


