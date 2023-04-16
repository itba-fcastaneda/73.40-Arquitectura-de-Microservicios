Para ejecutar el server

```
docker-compose up -d --build
```

Con el server corriendo, agregar lgunos datos en el DB
```
docker-compose exec api python manage.py recreate_db
docker-compose exec api python manage.py seed_db
```

Probar que se puede acceder al server con:
```
http://localhost:5004/zones
``` 

Ejecutar los tests:
```
docker-compose exec api python -m pytest "src/tests" -p no:warnings
```

Verificar la covertura:
```
docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src"
```

Pruebas de linting:
```
docker-compose exec api flake8 src
```

Testear el formateo de código:
```
docker-compose exec api black src --check
docker-compose exec api isort src --check-only
```
Para corregir el formato:
```
docker-compose exec api black src
docker-compose exec api isort src
```

