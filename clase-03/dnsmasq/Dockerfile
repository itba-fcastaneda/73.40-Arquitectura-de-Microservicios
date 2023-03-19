## Imagen de base, podría tener un tag para fijar la versión
## entre distintas corridas.
FROM alpine:3.11

## VARIABLES Y CONSTANTES
ARG DEFAULT_PORT=5353
ARG ENTRYPOINT=entry.sh
ARG DEFAULT_DNS_CONFIG=/etc/dnsmasq.conf
ARG DEFAULT_DNS_VOLUME=/etc/dnsmasq.d
ARG DEFAULT_DNS_HOSTS_FILE=${DEFAULT_DNS_VOLUME}/hosts

ENV DNS_CONFIG=${DEFAULT_DNS_CONFIG}
ENV DNS_VOLUME==${DEFAULT_DNS_VOLUME}
ENV DNS_HOSTS_FILE=${DEFAULT_DNS_HOSTS_FILE}
ENV DNS_PORT=${DEFAULT_PORT}
ENV DNS_ARGS="--conf-dir=${DNS_VOLUME} -d " 
## LABELS
LABEL maintainer=fcastaneda@itba.edu.ar

## PORT
EXPOSE ${DEFAULT_PORT}

## CREACIÓN DE LOS VOLÚMENES
RUN mkdir -p ${DNS_VOLUME}
VOLUME ${DNS_VOLUME}

## PREPARACIÖN DE LOS PROGRAMAS
RUN apk update && apk add dnsmasq && rm ${DEFAULT_DNS_CONFIG} && touch ${DEFAULT_DNS_CONFIG}
ADD ./${ENTRYPOINT} /${ENTRYPOINT}
RUN chmod a+x /${ENTRYPOINT}

ENTRYPOINT /entry.sh

## Cómo probarlo?
## docker build -t dnsmasq .
## docker run --rm -p 6000:5353/udp dnsmasq 
## dig @localhost -p 6000  www.google.com