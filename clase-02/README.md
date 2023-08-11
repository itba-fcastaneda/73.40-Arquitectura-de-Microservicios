# Arquitectura de Microservicios

## Entendiendo como Docker funciona por dentro

### Usuarios

Si nosotros pensamos a los contenedores como maquinas virtuales podriamos concluir que los usuarios que van a existir dentro de los mismos no tienen ningun tipo de conexion con los usuarios del host. En el caso de los contenedores, el proceso que se va a estar ejecutando lo estara haciendo de forma directa sobre el host. Hagamos algunas pruebas para verificarlo.

```bash
docker run -d ubuntu:latest sleep 500
ps uxa | grep sleep
```

Al hacer ps en el host podemos ver como aparece el proceso de sleep que ejecutamos dentro del container. Algo que llama la atencion es que el proceso esta siendo corrido por el usuario root. Esto se debe a que los containers utilizan el mismo sistema de UIDs que el kernel host. Por defecto al ejecutar un container este tomara el valro 0 asociado al usuario root. Podemos ver como esto cambia utilizando el flag `--user <name|uid>`

```bash
docker run -d --user 1234 ubuntu:latest sleep 500
ps uxa | grep sleep
```

Podemos ver como el proceso actual aparece con el usuario 1234, el mismo que indicamos antes. Asi como en este caso usamos el userID 1234, se podria usar cualquier otro. Esta es una de las consideraciones a tener en cuenta a la hora de correr un container. Si bien son un proceso aislado, tiene cierto contacto con el host subyacente. Un caso donde hay que tener en cuenta los usuarios son los permisos de los archivos y directorios.

### Network

En el contexto de los microservicios y las aplicaciones en general, muchas veces queremos exponer servicios para que sean accedidos por otros servicios o usuarios finales. Para esto la opcion mas utilziada es exponer un puerto y comunicarse via TCP/UDP. Que sucede con los containers?

Asi como los containers estan aislados a nivel filesystem y proceso tambien lo estan a nivel networking. Cada container tendra su propia interfaz de red. A su vez, docker nos permite generar multiples redes virtuales, permitiendo aislar a los contenedores del resto.

Teniendo en cuenta esto, como es posible acceder a los contenedores? Es siquiera posible?

Vamos a crear levantar un contenedor con un nginx adentro y vamos a verificarlo.

```bash
docker run --name web_server -d nginx
sudo ln -sf /proc/$(docker inspect -f '{{.State.Pid}}' web_server)/ns/net /var/run/netns/mycontainer; sudo ss -tln -N mycontainer ; sudo rm /var/run/netns/mycontainer
```

Despues de haberme mandado su contraseña con ese segundo comando, deberian ver que en el purto 80 hay un proceso escuchando. Lo que estamos haciendo ahi es analizando los puertos ocupados en la interfaz de red del container. Nginx esta corriendo y esperando conexiones. Si en vez de correr el segundo comando corremos `ss -nlt` en nuestro host veremos que no hay nadie en el puerto 80. Como podemos hacer para llegar?

Si bien no lo vemos a simple vista, el contenedor forma parte de una red virtual de nuestro host y el proceso esta escuchando en todas las interfaces `0.0.0.0:80`. Teniendo en cuenta que la red esta dentro del host y conociendo la IP del contenedor deberiamos poder llegar al nginx. 

```bash
curl $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Efectivamente pudimos acceder al servidor. Esto se debe a que lso container formen parte del host y no sean una abstracion completamente separada. Entonces, si desde el host puedo llegar, donde esta la aislacion? La aislacion que nos interesa es en relacion a otros contenedores, no al host en si. Para eso veamos un ejemplo.

Con el nginx corriendo deberian poder acceder al mismo de la siguiente forma:

```bash
docker run --rm curlimages/curl --silent $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Si dijimos que se aislaba el contenedor de otros contenedores, por que estamos llegando? Si bien a veces es de interes estar aislado, otras veces es de interes acceder otros servicios. Para ello se pueden generar redes que contengan 1 o mas contenedores. Podemos ver que, si creamos una nueva red y levantamos el contenedor de curl en la misma, este no llegara al nginx.

```bash
docker run --rm --network lonely_curl curlimages/curl -v -m 5 $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Podemos ver como ahora el curl no funciona y corta por timeout.

```bash
docker run - wbitt/network-multitool ip a
docker run --network lonely_curl wbitt/network-multitool ip a
```

Con estos dos comandos podemos verificar que los containers que se generan dentro de la red lonely_curl efectivamente tienen una red distinta a los que no. Impidiendo la comunicacion entre los mismos.

Pueden limpiar todos los contenedores que se generaron en el camino con `docker rm -f $(docker ps -aq)` 

### Contenido extra recomendado

[Containers From Scratch • Liz Rice • GOTO 2018](https://www.youtube.com/watch?v=8fi7uSYlOdc)

Presentacion de 35 minutos donde se muestar de manera simplificada como se puede construit una herramienta equivalente a los contenedores. Esta bueno para ver como son utilizadas las primitivas del sistema operativo para lograr el objetivo.

[How containers work: overlayfs](https://jvns.ca/blog/2019/11/18/how-containers-work--overlayfs/)

Articlo escrito por Julia Evans donde presenta el driver de filesystem overlay con pequeños ejemplos. OverlayFS es otro componente central de los contenedores. Permitiendo la modularizacion y reutilizacion de archivos. Recomiendo seguir los ejemplos plracticos y ver como funciona, es bastante llamativo.
