Para crear un certificado autofirmado. 

Ejecutar:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt
```
Usar pact-nginx como `Common Name`. No hacer falta ingresar nada en el resto de los campos. 
