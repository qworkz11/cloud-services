# Cloud Services

Multiple docker-based services behind a Traefik reverse proxy.

## Stages

Each service is located in a separate directory. Each service uses 3 stages:

### Dev

Standalone service. Run via 

```shell
docker-compose -f <service-name>.docker-compose.yaml -f compose.override.yaml
```

Ports are mapped to `localhost` and the service is reachable via `localhost`. No volume mounts are used, so data is volatile .

### Test

Service which relies on `traefik` as a reverse proxy, which is reachable via `localhost`. Each service requires a hostname to be set via label in the docker-compose/override file:

```yaml
...
labels:
    ...
    - traefik.http.routers.<router_name>.rule=Host(`$ENV-VAR`)
```

`ENV-VAR` must be set **in traefik's .env file**. This way, the host name can be kept secret when e.g. publishing on GitHub.

The test stage uses volume mounts, so data is persistent.

### Prod

Production system with proper usage of TLS etc. Still WIP...

## Service Structure

Each service is defined in `service-root/dev/service-name.docker-compose.yaml`. This `docker-compose`-file serves as the base definition. Each stage overrides or extends this base definition. Sensible data is kept in `.env` files. This creates the following directory structure:

```shell
service-root
    |-dev
        |-service-name.docker-compose.yaml
        |-override.docker-compose.yaml
    |-test
        |-service-name.docker-compose.yaml
        |-override.docker-compose.yaml
        |-.env
    |-prod
        |-service-name.docker-compose.yaml
        |-override.docker-compose.yaml
        |-.env
```

`docker-compose`-files in `test` and `prod` stages only need to include the service's base `docker-compose` file:

```yaml
# e.g. service-root/test/service-name.docker-compose.yaml
version: "3"

include:
    - ../dev/service-name.docker-compose.yaml
```

Everything else is managed in a `compose.override.yaml`, which only specifies the necessary changes and additions compared to the base service definition.