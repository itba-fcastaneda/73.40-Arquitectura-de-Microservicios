## Greetings

Greeting es un servicio dado por un contenedor a un cliente RPC. Usan Nameko para implementer RPC, y necesitan por lo tanto onua cola de mensajes de AMQP.

El objetivo es crear un Dockerfile para el service y otro para el consumer, de modo que cada uno pueda funcionar en su contenedor. Se adjunta el código en pything, los requerimientos para que funcion y el entrypoint.sh que se desea ejecutar.

Debe crear un docker-compose para ejecutar el service, y dejar al consumer corriendo de como que con un `docker exec` se pueda ejecutar el archivo consumer.py

Para implementar la cola AMQP pueden usar una instancia de RabbitMQ cuya configuración deben compartir con ambos contenedores. 

Para su referencia:
* https://x-team.com/blog/set-up-rabbitmq-with-docker-compose
* https://betterprogramming.pub/building-microservices-with-nameko-c2ddd203130b
* https://medium.com/fintechexplained/running-python-in-docker-container-58cda726d574
