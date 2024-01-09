PROJECT_NAME := keystrokes-recognition

.PHONY: up-deps
up-deps:
	docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		up

.PHONY: stop
stop:
	docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		stop

.PHONY: down
down:
	docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		down
