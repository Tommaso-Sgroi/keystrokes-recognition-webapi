PROJECT_NAME := keystrokes-recognition

.PHONY: up-deps
up-deps:
	docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		up

.PHONY: stop
stop:
	DOCKER_IMAGE=${DOCKER_IMAGE_PATH}:${DOCKER_IMAGE_TAG} \
		docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		-f dependencies/docker-compose.cicd.yml \
		stop

.PHONY: down
down:
	DOCKER_IMAGE=${DOCKER_IMAGE_PATH}:${DOCKER_IMAGE_TAG} \
		docker compose -p ${PROJECT_NAME} \
		-f dependencies/docker-compose.yml \
		-f dependencies/docker-compose.cicd.yml \
		down
