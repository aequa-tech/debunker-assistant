# DEBUNKER-ASSISTANT

_insert project description_

## Installation
To start the project, Docker (or Docker Desktop) must be installed on your machine [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

**Customization of docker-compose.yml**
The internal Debunker-Assistant APIs use Basic Auth.
Therefore, it is necessary to import the environment variables `DEBUNKER_USERNAME` and `DEBUNKER_PASSWORD` within the `environment` section of the `debunker` service in the `docker-compose.yml` file.

**Starting the project**
`docker compose up --build`

## Usage
Debunker-Assistant exposes the service on port 8080.
You can therefore query the internal APIs using `localhost:8080` as the host.

The service exposes 3 API routes:
- _POST_ **scrape** `localhost:8080/internal/v1/scrape`
- _GET_ **evaluation** `localhost:8080/internal/v1/evaluation`
- _GET_ **explanations** `localhost:8080/internal/v1/explanations`

The complete API documentation is available in the `reference.yml` file (OpenApi 3.x specification).

## Contributing
_insert text_

## License
_insert text_

## Contact
_insert text_
