## Entrypoint

## Vars from Dockerfile
# ENV DNS_VOLUME=/etc/dnsmasq.d
# ENV DNS_PORT=${DEFAULT_PORT}
# ENV DNS_CONFIG=${DEFAULT_DNS_CONFIG}

## Preparo la configuración config
if [ -z "${DNS_PORT}" ]; then
    DNS_PORT=5353
fi
DNS_ARGS="${DNS_ARGS} -p ${DNS_PORT}"

## Ejecutar dnsmasq
echo "Starting dnsmask listening in port ${DNS_PORT}"
dnsmasq ${DNS_ARGS} 