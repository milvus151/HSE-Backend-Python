COMPOSE_DB = docker-compose -f store/docker-compose.yaml
COMPOSE_APP = docker-compose -f service/docker-compose.yaml

start:
	$(COMPOSE_DB) up -d
	$(COMPOSE_APP) up -d --build

stop:
	-$(COMPOSE_APP) down
	-$(COMPOSE_DB) down

migrations:
	docker exec -it hw5_django python manage.py makemigrations
	docker exec -it hw5_django python manage.py migrate

superuser:
	docker exec -it hw5_django python manage.py createsuperuser

logs:
	docker logs -f hw5_django
