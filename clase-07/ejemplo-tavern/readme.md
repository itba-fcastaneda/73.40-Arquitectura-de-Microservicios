Para ejecutar:

´´´
pipenv install requirements.txt
pipenv shell

export FLASK_APP=server.py
flask run
´´´

Para probar, con el server corriendo:
```
python -m pytest test
```