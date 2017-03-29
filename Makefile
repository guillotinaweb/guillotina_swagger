
setup:
	curl -X POST -H "Accept: application/json" --user root:root -H "Content-Type: application/json" -d '{"@type": "Container","title": "Container","id": "container","description": "Description"}' "http://127.0.0.1:8080/db/"

run-postgres:
	docker run -e POSTGRES_DB=guillotina -e POSTGRES_USER=postgres -p 127.0.0.1:5432:5432 postgres:9.6
