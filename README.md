# YouCalendar
### Requirements
* `Python 3.10+`
* `Docker`
---
### Setup
* In `./` create an `api.env` file and specify your API key and AUTH token:
```
API_KEY=<your YouTube API key>
AUTH_TOKEN=<your unique authorisation token>
```
---
### Start
* `docker-compose up -d`
---
### Usage
* Add channel
* Delete channel
* Get channel
* Get all channels
---
### Helpfull stuff
* Docker reset: `docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) && docker rmi -f $(docker images -q) && docker system prune && docker-compose up -d`