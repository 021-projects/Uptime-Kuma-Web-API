# Uptime-Kuma-Web-API

## A REST API wrapper for [Uptime Kuma](https://github.com/louislam/uptime-kuma) using [Uptime-Kuma-API](https://github.com/lucasheld/uptime-kuma-api)

---

## Endpoints:

![1](./images/1.png)
![2](./images/2.png)
![3](./images/3.png)
![4](./images/4.png)

## How to use it:
```bash
git clone https://github.com/021-projects/Uptime-Kuma-Web-API.git
cd Uptime-Kuma-Web-API
git checkout develop
./setup.sh
./run.sh
```

## How to use it with Docker:

---

### Environment Variables :

#### Required
You have to define these ENV VARS in order to connect to your KUMA server.

    KUMA_SERVER: The URL of your Uptime Kuma instance. ex: https://uptime.example.com
    KUMA_USERNAME: The username of your Uptime Kuma user
    KUMA_PASSWORD: The password of your Uptime Kuma user
    ADMIN_PASSWORD: An admin password to access the API

#### Optional
Additional configuration variables available

    KUMA_WAIT_EVENTS: Time in seconds to wait for events to be processed. Defaults to 0.2 second.
    ACCESS_TOKEN_EXPIRATION: Minutes the access token should be valid. Defaults to 8 days.
    SECRET_KEY: A secret value to encode JWTs with

#### Note:

You have to define your ADMIN_PASSWORD or you wont be able to connect to your rest api.

You will connect with those credentials:

    username = admin
    password = <ADMIN_PASSWORD>

### Features:

- Multi user Kuma api ( without privilege YET!!) with a small SQLite db
- Easy to use REST API with most of the Uptime-Kuma features
- Swagger Docs
- Dockerized [UptimeKuma_RestAPI Image](https://hub.docker.com/r/alexdresko/uptimekuma_restapi)
- Multi-architecture support (amd64, arm64)

### Example :

You can simply create a docker compose file like this :

```yaml
services:
  kuma:
    container_name: uptime-kuma
    image: louislam/uptime-kuma:latest
    ports:
      - "3001:3001"
    restart: always
    volumes:
      - uptime-kuma:/app/data

  api:
    container_name: backend
    image: alexdresko/uptimekuma_restapi
    volumes:
      - api:/db
    restart: always
    environment:
      - KUMA_SERVER=http://kuma:3001
      - KUMA_USERNAME=test
      - KUMA_PASSWORD=123test.
      - ADMIN_PASSWORD=admin
    depends_on:
      - kuma
    ports:
      - "8000:8000"

volumes:
  uptime-kuma:
  api:
```

### In order for the example to work: You have to run kuma first then create your kuma username and password then re-run the compose file.

### Example CURL Script:

---

```bash
TOKEN=$(curl -L -X 'POST' -H 'Content-Type: application/x-www-form-urlencoded' --data 'grant_type=password&username=admin&password=admin' http://127.0.0.1:8000/login/access-token/ | jq -r ".access_token")
curl -L -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:8000/monitors/
```
