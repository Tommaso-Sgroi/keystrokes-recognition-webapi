# keystrokes-recognition-webapi
Backend for the Biometric Systems demo project

## Project structure

* `main` is the executive file for start the webapi server
* `db/` is the directory for database schema
* `doc/` contains the documentation for APIs, this means an OpenAPI file
* `service/` has all packages for implementing project-specific functionalities
	* `service/api` contains API endpoints server
	* `service/database` contains the database connection class for executing queries
	* `service/keystroke_recognition` contains a wrapper for our Keras keystrokes recognition model

Other project files include:
* `Dockerfile` contains specs for building OCI containers
* `config.json` contains the configuration for DB, API and model
* `Makefile` contains some useful targets:
	* `up-deps` starts all dependencies for local development/demo using `docker compose`
	* `down` destroys all containers started using `up-deps`

## How to run?
Simply execute the main file with python >= 3