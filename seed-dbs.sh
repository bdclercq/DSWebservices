docker-compose -f docker-compose-dev.yml run stops python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run stops python manage.py seed-db

docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run users python manage.py seed-db

docker-compose -f docker-compose-dev.yml run vehicles python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run vehicles python manage.py seed-db

docker-compose -f docker-compose-dev.yml run ratings python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run ratings python manage.py seed-db

