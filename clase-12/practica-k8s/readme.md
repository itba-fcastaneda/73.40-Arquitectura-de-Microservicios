# Práctica Kubernetes

## Instalar kubectl

Kubectl es una interfaz de línea de comandos para ejecutar comandos sobre despliegues clusterizados de Kubernetes. Esta interfaz es la manera estándar de comunicación con el clúster ya que permite realizar todo tipo de operaciones sobre el mismo.

``` bash
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

Si desean pueden definir algunos alias en el shell para acceder a kubectl. Vean el [link](https://raw.githubusercontent.com/ahmetb/kubectl-aliases/master/.kubectl_aliases)

## Instalar minikube


Para AMD64
``` bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Para ARM64
``` bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-arm64
sudo install minikube-linux-arm64 /usr/local/bin/minikube
```

## Iniciar el cluster

```bash
minikube start
```

El proceso tarde un ratito pero al final debería ver esto:

```
fede@lincon:~$ minikube start
😄  minikube v1.30.1 on Ubuntu 22.04 (arm64)
✨  Automatically selected the docker driver. Other choices: none, ssh
📌  Using Docker driver with root privileges
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.26.3 preload ...
    > preloaded-images-k8s-v18-v1...:  330.52 MiB / 330.52 MiB  100.00% 8.25 Mi
    > gcr.io/k8s-minikube/kicbase...:  336.39 MiB / 336.39 MiB  100.00% 4.87 Mi
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  Preparing Kubernetes v1.26.3 on Docker 23.0.2 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🔎  Verifying Kubernetes components...
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Con esto tiene un cluster de k8s 100% funcional corriendo en su máquina. 

Pueden confirmar la ejecución viendo los contenedores:

```
fede@lincon:~$ docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED         STATUS         
e1ce0ab7a600   gcr.io/k8s-minikube/kicbase:v0.0.39   "/usr/local/bin/entr…"   2 minutes ago   Up 2 minutes   127.0.0.1:49157->22/tcp, 127.0.0.1:49156->2376/tcp, 127.0.0.1:49155->5000/tcp, 127.0.0.1:49154->8443/tcp, 127.0.0.1:49153->32443/tcp   minikube
```

## Recorriendo el cluster

### Conexión a la API de cluster

Kubectl es una herramienta de CLI utilizada para interactuar con el clúster de Kubernetes. Kubectl actúa como un cliente para la API de Kubernetes. Al ejecutar comandos con kubectl, estás enviando solicitudes a la API de Kubernetes. Estas solicitudes pueden incluir crear, leer, actualizar o eliminar recursos en el clúster, como pods, servicios, despliegues, entre otros. Kubectl envía las solicitudes a través de la red hacia el servidor de la API de Kubernetes.

La API de Kubernetes procesa las solicitudes y realiza las operaciones correspondientes en el clúster. Luego, envía una respuesta a kubectl, que la muestra en la salida de la línea de comandos. Esto permite a los usuarios interactuar con el clúster de Kubernetes y administrar sus aplicaciones y recursos de forma eficiente.

``` bash
fede@lincon:~$ cat .kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /home/fede/.minikube/ca.crt
    extensions:
    - extension:
        last-update: Fri, 02 Jun 2023 11:58:00 UTC
        provider: minikube.sigs.k8s.io
        version: v1.30.1
      name: cluster_info
    server: https://192.168.49.2:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    extensions:
    - extension:
        last-update: Fri, 02 Jun 2023 11:58:00 UTC
        provider: minikube.sigs.k8s.io
        version: v1.30.1
      name: context_info
    namespace: default
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/fede/.minikube/profiles/minikube/client.crt
    client-key: /home/fede/.minikube/profiles/minikube/client.key
```

Esta es la dirección donde está la API del cluster `server: https://192.168.49.2:8443`. 

Las credenciales de autenticación están basadas en certificados digitales. 

```
  user:
    client-certificate: /home/fede/.minikube/profiles/minikube/client.crt
    client-key: /home/fede/.minikube/profiles/minikube/client.key
```

Pueden conectarse directamente a la API con curl:

``` bash
curl https://192.168.49.2:8443/version --cert ~/.minikube/profiles/minikube/client.crt --key  ~/.minikube/profiles/minikube/client.key --cacert ~/.minikube/ca.crt
```

Y verán:

```json
{
  "major": "1",
  "minor": "26",
  "gitVersion": "v1.26.3",
  "gitCommit": "9e644106593f3f4aa98f8a84b23db5fa378900bd",
  "gitTreeState": "clean",
  "buildDate": "2023-03-15T13:33:12Z",
  "goVersion": "go1.19.7",
  "compiler": "gc",
  "platform": "linux/arm64"
}
```

Que es la misma información que vemos con el kubectl

``` bash
fede@lincon:~$ kubectl version
WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.  Use --output=yaml|json to get the full version.
Client Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.2", GitCommit:"7f6f68fdabc4df88cfea2dcf9a19b2b830f1e647", GitTreeState:"clean", BuildDate:"2023-05-17T14:20:07Z", GoVersion:"go1.20.4", Compiler:"gc", Platform:"linux/arm64"}
Kustomize Version: v5.0.1
Server Version: version.Info{Major:"1", Minor:"26", GitVersion:"v1.26.3", GitCommit:"9e644106593f3f4aa98f8a84b23db5fa378900bd", GitTreeState:"clean", BuildDate:"2023-03-15T13:33:12Z", GoVersion:"go1.19.7", Compiler:"gc", Platform:"linux/arm64"}
```

### APIs

Si queremos ver todas las APIs que están habilitadas en un cluter podemos ejecutar 

```bash
fede@lincon:~$ kubectl api-versions

admissionregistration.k8s.io/v1
apiextensions.k8s.io/v1
apiregistration.k8s.io/v1
apps/v1
authentication.k8s.io/v1
authorization.k8s.io/v1
autoscaling/v1
autoscaling/v2
batch/v1
certificates.k8s.io/v1
coordination.k8s.io/v1
discovery.k8s.io/v1
events.k8s.io/v1
flowcontrol.apiserver.k8s.io/v1beta2
flowcontrol.apiserver.k8s.io/v1beta3
networking.k8s.io/v1
node.k8s.io/v1
policy/v1
rbac.authorization.k8s.io/v1
scheduling.k8s.io/v1
storage.k8s.io/v1
storage.k8s.io/v1beta1
v1
```

Y para ver los recursos controlado por cada API

```bash
fede@lincon:~$ kubectl api-resources |grep app
controllerrevisions                  apps/v1              true         ControllerRevision
daemonsets              ds           apps/v1              true         DaemonSet
deployments             deploy       apps/v1              true         Deployment
replicasets             rs           apps/v1              true         ReplicaSet
statefulsets            sts          apps/v1              true         StatefulSet
```

### Apply & Diff

Creen un archivo y nombrenlo `simple-pod.yaml`. Agreguen el siguiente contenido:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

Pueden aplicar los cambios en la API con `kubectl apply -f simple-pod.yaml`. Deberían ver el siguiente output:

```bash
fede@lincon:~$ kubectl apply -f simple-pod.yaml
pod/nginx created
```

Si queremos ver la definición completa del pod, pueden verla con `kubectl get pod nginx -o yaml` y pueden ver que será muchas más definiciones que las que inicialmente tenía el archivo.

Cambien ahora la versión del la imagen del contenedor por `1.13.1`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.13.1
    ports:
    - containerPort: 80
```

Pueden ver la diferencia entre el nuevo manifiesto y lo que está aplicado con un `kubectl diff -f simple-pod.yaml`. 

```bash
fede@lincon:~$ kubectl diff -f simple-pod.yaml
diff -u -N /tmp/LIVE-1797837909/v1.Pod.default.nginx /tmp/MERGED-3198508001/v1.Pod.default.nginx
--- /tmp/LIVE-1797837909/v1.Pod.default.nginx	2023-06-03 22:09:38.052587820 +0000
+++ /tmp/MERGED-3198508001/v1.Pod.default.nginx	2023-06-03 22:09:38.052587820 +0000
@@ -11,7 +11,7 @@
   uid: 23479b9a-40b6-4123-9f7d-76c82f74d321
 spec:
   containers:
-  - image: nginx:1.14.2
+  - image: nginx:1.13.1
     imagePullPolicy: IfNotPresent
     name: nginx
     ports:
```

### Controllers

Cada controller en el clúster es un cliente de la API, y por lo tanto tiene su identidad y service account. Para ver todos los controllers se puede hacer: 

```bash
fede@lincon:~$ kubectl get sa -n kube-system

NAME                                 SECRETS   AGE
attachdetach-controller              0         35h
bootstrap-signer                     0         35h
certificate-controller               0         35h
clusterrole-aggregation-controller   0         35h
coredns                              0         35h
cronjob-controller                   0         35h
daemon-set-controller                0         35h
default                              0         35h
deployment-controller                0         35h
disruption-controller                0         35h
endpoint-controller                  0         35h
endpointslice-controller             0         35h
endpointslicemirroring-controller    0         35h
ephemeral-volume-controller          0         35h
expand-controller                    0         35h
generic-garbage-collector            0         35h
horizontal-pod-autoscaler            0         35h
job-controller                       0         35h
kube-proxy                           0         35h
namespace-controller                 0         35h
node-controller                      0         35h
persistent-volume-binder             0         35h
pod-garbage-collector                0         35h
pv-protection-controller             0         35h
pvc-protection-controller            0         35h
replicaset-controller                0         35h
replication-controller               0         35h
resourcequota-controller             0         35h
root-ca-cert-publisher               0         35h
service-account-controller           0         35h
service-controller                   0         35h
statefulset-controller               0         35h
storage-provisioner                  0         35h
token-cleaner                        0         35h
ttl-after-finished-controller        0         35h
ttl-controller                       0         35h
```

### Debug desde adentro del clúster

Poder probar cosas desde adentro del cluster pueden ejecutar un contenedor on-deman por afuera del proceso declarativo con: 

```bash
kubectl run -i --rm --tty debug --image=busybox --restart=Never -- sh
```

Este comando ejecuta un pod en forma interactiva usando una image de busybox. Al finalizar la ejecución el Pod es destruido. 

Parados el pod podemos alcanzar la IP y puertos de cualquier Pod corriendo.


### Namespaces

Un namespace en Kubernetes es una forma de organizar y dividir los recursos dentro de un clúster de Kubernetes. Proporciona un ámbito aislado para los objetos, como los pods, los servicios y los volúmenes, lo que permite la segmentación lógica y la gestión más eficiente de los recursos.

Cada namespace actúa como un contenedor lógico dentro del clúster de Kubernetes, lo que significa que los objetos en un namespace no se mezclan con los objetos en otros espacios de nombres. Esto permite que diferentes equipos o aplicaciones compartan el mismo clúster sin interferir entre sí.

Los espacios de nombres también ayudan a evitar colisiones de nombres, ya que los objetos en diferentes espacios de nombres pueden tener los mismos nombres sin conflictos. Esto facilita la gestión de aplicaciones complejas y de múltiples equipos dentro de un clúster de Kubernetes.

``` bash
fede@lincon:~$ kubectl get namespaces
NAME                   STATUS   AGE
default                Active   30m
kube-node-lease        Active   30m
kube-public            Active   30m
kube-system            Active   30m
kubernetes-dashboard   Active   24m
```

### ReplicaSet

Un ReplicaSet en Kubernetes es un objeto que permite garantizar la disponibilidad y la escalabilidad de las aplicaciones en un clúster. Es una abstracción que define un conjunto de réplicas de un Pod (unidad mínima en Kubernetes) y asegura que siempre haya una cantidad específica de réplicas en funcionamiento.

El ReplicaSet monitorea constantemente el estado de las réplicas y, en caso de que alguna de ellas falle o sea eliminada, se encarga de crear automáticamente nuevas réplicas para reemplazarlas. Esto garantiza que la aplicación siga funcionando correctamente incluso en situaciones de fallas o interrupciones.

Además, el ReplicaSet permite escalar vertical u horizontalmente la cantidad de réplicas de un Pod. Esto significa que se puede aumentar o disminuir la cantidad de réplicas en función de la carga de trabajo o los recursos disponibles, lo que permite adaptar la capacidad de la aplicación a las necesidades cambiantes.

Configurar y desplegar este replica set:

`simple-rs.yaml`
``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web
  labels:
    env: dev
    role: web
spec:
  replicas: 3
  selector:
    matchLabels:
      role: web
  template:
    metadata:
      labels:
        role: web
    spec:
      containers:
      - name: testnginx
        image: nginx
```

Se puede ver la definicón del criterio de adopción de Pods está definido por el `selector`:

``` yaml
  selector:
    matchLabels:
      role: web
```

Aplicamos el manifiesto `kubectl apply -f simple-rs.yaml` y vemos los Pods creados: 

``` bash
fede@lincon:~$ kubectl get rs
NAME   DESIRED   CURRENT   READY   AGE
web    3         3         3       4m41s

fede@lincon:~$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
web-npdvz   1/1     Running   0          5m25s
web-t78vj   1/1     Running   0          5m25s
web-vtl5s   1/1     Running   0          5m25s
```

Si borramos un pod, otro inmediatamente toma su lugar:

``` bash
fede@lincon:~$ kubectl delete pod web-t78vj ; kubectl get pods
pod "web-t78vj" deleted
NAME        READY   STATUS              RESTARTS   AGE
web-gv8zj   0/1     ContainerCreating   0          1s
web-npdvz   1/1     Running             0          6m36s
web-vtl5s   1/1     Running             0          6m36s
fede@lincon:~$ kubectl get pods
NAME        READY   STATUS              RESTARTS   AGE
web-gv8zj   0/1     ContainerCreating   0          3s
web-npdvz   1/1     Running             0          6m38s
web-vtl5s   1/1     Running             0          6m38s
fede@lincon:~$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
web-gv8zj   1/1     Running   0          4s
web-npdvz   1/1     Running   0          6m39s
web-vtl5s   1/1     Running   0          6m39s
```

Si analizamos uno de los pods podemos ver que el ReplicaSet es el owner del pod:

```bash
kubectl get pods web-vtl5s -o yaml | grep -A 5 owner

  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: web

```

Vamos a crear un pod manulamente:

`pod_orphan.yaml`
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: orphan
  labels:
    role: web
spec:
  containers:
  - name: orphan
    image: httpd
```

Al aplicar el pod podemos ver que automaticamente es borrado por el replica set, ya que al ver que tiene ya la cantidad de pods deseada, aquellos que coinciden con el selector, son considerados innecesarios, y se eliminan.

```bash
fede@lincon:~$ kubectl get pods
NAME        READY   STATUS        RESTARTS   AGE
orphan      0/1     Terminating   0          1s
web-gv8zj   1/1     Running       0          8m8s
web-npdvz   1/1     Running       0          14m
web-vtl5s   1/1     Running       0          14m
```

En cambio, si el pod estuviera corriendo antes de inicial el replica set, es adoptado y agregado a la lista de los pods controlados.

Borramos el ReplicaSet `kubectl delete rs web`, creamos el Pod y confirmamos que está corriendo. Vemos que no tiene `owner`
```bash
fede@lincon:~$ kubectl apply -f pod_orphan.yaml
pod/orphan created
fede@lincon:~$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
orphan   1/1     Running   0          6s
fede@lincon:~$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
orphan   1/1     Running   0          11s
fede@lincon:~$ kubectl get pods orphan -o yaml | grep -A 5 owner
fede@lincon:~$ 
```

Creamos el ReplicaSet y luegos de unos segundo vemos que el pod fue adoptado:

```bash
fede@lincon:~$ kubectl apply -f simple-rs.yaml
replicaset.apps/web created
fede@lincon:~$ kubectl get rs
NAME   DESIRED   CURRENT   READY   AGE
web    3         3         3       7s
fede@lincon:~$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
orphan      1/1     Running   0          38s
web-n4wbc   1/1     Running   0          12s
web-vdkf6   1/1     Running   0          12s
fede@lincon:~$ kubectl get pods orphan -o yaml | grep -A 5 owner
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: web
```

El destino de los pods adoptados pasa a ser el mismo del ReplicaSet. Si borro el ResplicaSet, todos los recursos gestionados serán borrados. 

```bash
fede@lincon:~$ kubectl delete rs web
replicaset.apps "web" deleted
fede@lincon:~$ kubectl get pods
No resources found in default namespace.
```

En caso de querer borrar el ReplicaSet pero no los pods, se puede usar la opción `--cascade=orphan`, que le da independencia a los pods, que luego debe ser borrados en forma independiente.


```bash
fede@lincon:~$ kubectl delete rs web --cascade=orphan
replicaset.apps "web" deleted
fede@lincon:~$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
orphan      1/1     Running   0          8m56s
web-69dcw   1/1     Running   0          69s
web-lrhtt   1/1     Running   0          69s
fede@lincon:~$ kubectl get pods orphan -o yaml | grep -A 5 owner
```

En resumen, un ReplicaSet en Kubernetes es un componente esencial para garantizar la disponibilidad, la tolerancia a fallos y la escalabilidad de las aplicaciones en un clúster, al mantener un conjunto de réplicas de los Pods y gestionar su estado de manera automática.

### Deployments

Un deployment en Kubernetes es un componente fundamental que permite administrar y controlar la ejecución de aplicaciones dentro de un clúster de Kubernetes. En pocas palabras, se refiere al proceso de despliegue y gestión de aplicaciones en contenedores en un entorno de Kubernetes.

En un deployment, se define una especificación que describe cómo debe ser ejecutada la aplicación en el clúster. Esta especificación incluye detalles sobre la imagen del contenedor, la cantidad de réplicas que se deben crear, los recursos que se asignarán a cada réplica y otras configuraciones relacionadas.

Cuando se crea un deployment, Kubernetes se encarga de crear y gestionar los recursos necesarios para ejecutar la aplicación. Esto implica la creación de réplicas del contenedor, la asignación de recursos, la distribución de carga, la supervisión de la salud de las réplicas y la implementación de actualizaciones de manera controlada.

Una vez que se ha creado un deployment, Kubernetes garantiza que la cantidad especificada de réplicas esté siempre en funcionamiento. En caso de que una réplica falle o se deteriore, Kubernetes automáticamente creará una nueva réplica para reemplazarla y mantener la disponibilidad de la aplicación.

Vamos a definir un deployment en el archivo `deployment.yaml`.

```yaml                                                                                                28,20         All
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

A aplicarlo:

``` bash
fede@lincon:~$  kubectl apply -f deployment.yaml
deployment.apps/nginx created
fede@lincon:~$ kubectl get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           4s
fede@lincon:~$ kubectl get rs
NAME               DESIRED   CURRENT   READY   AGE
nginx-85996f8dbd   3         3         3       11s
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
nginx-85996f8dbd-2dqss   1/1     Running   0          14s
nginx-85996f8dbd-8w2v4   1/1     Running   0          14s
nginx-85996f8dbd-d8gmv   1/1     Running   0          14s
fede@lincon:~$
```

Podemos cambiar la cantidad de pods en el deployment cambiando el scale

``` bash
fede@lincon:~$ kubectl scale deploy nginx --replicas=2
deployment.apps/nginx scaled
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
nginx-85996f8dbd-8w2v4   1/1     Running   0          117s
nginx-85996f8dbd-d8gmv   1/1     Running   0          117s
```

Si vemos la descripción del pod

``` bash
kd pod nginx-85996f8dbd-qtpvv  | grep Image
    Image:          nginx:1.14.2
    Image ID:       docker-pullable://nginx@sha256:f7988fb6c02e0ce69257d9bd9cf37ae20a60f1df7563c3a2a6abe24160306b8d
```

La ventaja del Deployment sobre el ReplicaSet es la capacidad de hacer cambios en el despligue de la aplicación sin afectar el servicio. Por ejemplo: podemos actualizar la versión de de la imagen del Deployment y en forma prograsiva se irá actualizando cada uno de los pods. 

``` bash
fede@lincon:~$ kubectl set image  deploy/nginx nginx=nginx:1.24.0
deployment.apps/nginx image updated
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
nginx-7f68795f75-bq6wr   0/1     Terminating         0          83s
nginx-85996f8dbd-8w2v4   1/1     Running             0          12m
nginx-85996f8dbd-d8gmv   1/1     Running             0          12m
nginx-85996f8dbd-mmgc4   1/1     Running             0          8m9s
nginx-85996f8dbd-xhb5z   1/1     Running             0          8m9s
nginx-b55dcc56f-7qcf8    0/1     ContainerCreating   0          2s
nginx-b55dcc56f-dnjkw    0/1     ContainerCreating   0          2s
nginx-b55dcc56f-wtfv4    0/1     ContainerCreating   0          2s

fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
nginx-85996f8dbd-8w2v4   1/1     Running             0          12m
nginx-b55dcc56f-7qcf8    0/1     ContainerCreating   0          8s
nginx-b55dcc56f-b2h94    0/1     ContainerCreating   0          3s
nginx-b55dcc56f-dnjkw    1/1     Running             0          8s
nginx-b55dcc56f-jbttc    1/1     Running             0          5s
nginx-b55dcc56f-wtfv4    1/1     Running             0          8s

fede@lincon:~$ kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
nginx-b55dcc56f-7qcf8   1/1     Running   0          12s
nginx-b55dcc56f-b2h94   1/1     Running   0          7s
nginx-b55dcc56f-dnjkw   1/1     Running   0          12s
nginx-b55dcc56f-jbttc   1/1     Running   0          9s
nginx-b55dcc56f-wtfv4   1/1     Running   0          12s
fede@lincon:~$ kubectl describe pod nginx-b55dcc56f-wtfv4  | grep Image
    Image:          nginx:1.24.0
    Image ID:       docker-pullable://nginx@sha256:f3a9f1641ace4691afed070aadd1115f0e0c4ab4b2c1c447bf938619176c3eec
```

En forma progresive se fueron actualizando los Pods, y sólo al tener el pod nuevo activo se disparaba la destrucción del pod viejo. Si ponemos una imagen inválida:

``` bash
fede@lincon:~$ kubectl set image  deploy/nginx nginx=nginx:9.9.9
deployment.apps/nginx image updated
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
nginx-6776ff65cc-b4t5b   0/1     ContainerCreating   0          3s
nginx-6776ff65cc-gwbcl   0/1     ContainerCreating   0          3s
nginx-6776ff65cc-wshcs   0/1     ContainerCreating   0          3s
nginx-b55dcc56f-7qcf8    1/1     Running             0          2m41s
nginx-b55dcc56f-b2h94    1/1     Running             0          2m36s
nginx-b55dcc56f-jbttc    1/1     Running             0          2m38s
nginx-b55dcc56f-wtfv4    1/1     Running             0          2m41s
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
nginx-6776ff65cc-b4t5b   0/1     ErrImagePull        0          7s
nginx-6776ff65cc-gwbcl   0/1     ContainerCreating   0          7s
nginx-6776ff65cc-wshcs   0/1     ErrImagePull        0          7s
nginx-b55dcc56f-7qcf8    1/1     Running             0          2m45s
nginx-b55dcc56f-b2h94    1/1     Running             0          2m40s
nginx-b55dcc56f-jbttc    1/1     Running             0          2m42s
nginx-b55dcc56f-wtfv4    1/1     Running             0          2m45s
```

Los pods viejos no se destruyen hasta que los nuevos no está operativos, asegurando la disponibilidad de la aplicación.

Supongamos que tenemos un deployment estable:

``` bash
fede@lincon:~$ kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
nginx-b55dcc56f-2bbbw   1/1     Running   0          28m
nginx-b55dcc56f-7qcf8   1/1     Running   0          28m
nginx-b55dcc56f-b2h94   1/1     Running   0          28m
nginx-b55dcc56f-jbttc   1/1     Running   0          28m
nginx-b55dcc56f-wtfv4   1/1     Running   0          28m
```

Al hacer un cambio no deseado o que detectamos que no está funcionando correctamente, podemos hacer facilwmnte rollback.

``` bash
fede@lincon:~$ kubectl set image  deploy/nginx nginx=nginx:9.9.9
deployment.apps/nginx image updated
fede@lincon:~$ kubectl get pods
NAME                     READY   STATUS             RESTARTS   AGE
nginx-6776ff65cc-8d7pm   0/1     ErrImagePull       0          18s
nginx-6776ff65cc-nmrzr   0/1     ErrImagePull       0          18s
nginx-6776ff65cc-vkpdp   0/1     ImagePullBackOff   0          18s
nginx-b55dcc56f-7qcf8    1/1     Running            0          29m
nginx-b55dcc56f-b2h94    1/1     Running            0          29m
nginx-b55dcc56f-jbttc    1/1     Running            0          29m
nginx-b55dcc56f-wtfv4    1/1     Running            0          29m

fede@lincon:~$ kubectl rollout undo deployments/nginx
deployment.apps/nginx rolled back
fede@lincon:~$ kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
nginx-b55dcc56f-7qcf8   1/1     Running   0          29m
nginx-b55dcc56f-b2h94   1/1     Running   0          29m
nginx-b55dcc56f-fg8w2   1/1     Running   0          6s
nginx-b55dcc56f-jbttc   1/1     Running   0          29m
nginx-b55dcc56f-wtfv4   1/1     Running   0          29m
```

El ReplicaSet `nginx-6776ff65cc`, creado después de la modificación hecha en el deployment, fue destruido y se conservó el deployment original.

En resumen, un deployment en Kubernetes permite desplegar y gestionar aplicaciones en contenedores de manera eficiente, asegurando la escalabilidad, la alta disponibilidad y la gestión de recursos en un clúster de Kubernetes.

### DeamonSet

Un DaemonSet en Kubernetes es un tipo de controlador que garantiza que un pod se ejecute en todos los nodos disponibles en un clúster. A diferencia de otros controladores de replicación, como los ReplicationSets, que pueden crear y administrar múltiples instancias de un pod, un DaemonSet asegura que exactamente una instancia de un pod esté presente en cada nodo del clúster.

Cada vez que se agrega un nuevo nodo al clúster o se detecta la eliminación de un nodo, el DaemonSet automáticamente crea o destruye un pod en el nodo correspondiente. Esto garantiza que el pod esté en funcionamiento en todos los nodos y se ajuste al tamaño del clúster sin necesidad de intervención manual.

Los DaemonSets son útiles para implementar agentes de monitoreo, registradores de registros o servicios de red que necesitan ejecutarse en todos los nodos del clúster. Además, pueden utilizarse para tareas de administración del sistema, como recolectar métricas o realizar actualizaciones en todos los nodos.

Creamos el archivo `daemonset.yaml`:
``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: logger
  labels:
    app: logger
spec:
  selector:
    matchLabels:
      name: logger
  template:
    metadata:
      labels:
        name: logger
    spec:
      containers:
      - name: logger
        image: busybox
        command: ["sleep","infinity"]
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

Deplegamos y confirmamos que hay uno desplegado por nodo:

```bash
fede@lincon:~$ kubectl apply -f deamonset.yaml
daemonset.apps/logger created
fede@lincon:~$ kubectl get pods -o wide
NAME           READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
logger-bnxwc   1/1     Running   0          12m   10.244.0.70   minikube   <none>           <none>
```

De ahí podemos saltar dentro del pod y ver los logs del nodo.

```bash
fede@lincon:~$ kubectl exec -it logger-8l7wz -- ls /var/log/pods/
default_logger-bnxwc_965f0ad2-f1b5-45c3-a43f-9008666dbd46
default_nginx-b55dcc56f-fg8w2_1cf46795-d98c-4c5f-b2a1-3fdd36a1a183
default_nginx-b55dcc56f-wtfv4_eda35a99-4868-4f15-bcc9-de4ab7b30916
default_orphan_2077e337-4004-40e8-ba52-0c6d30318fd6
default_orphan_259ea237-13f3-4a72-8156-f1d024910081
default_orphan_8cf2cba6-c5a7-4f02-8ba6-cfffe4e42eb2
default_web-69dcw_0f85554e-d935-4be8-8e22-e71efb406e6e
default_web-gv8zj_201271ea-08df-4109-b432-b68eef298894
default_web-npdvz_cc9350ed-32b5-40d1-bd70-e0437110186f
default_web-vtl5s_c5569fb9-6790-4cca-b6bc-094083282c91
kube-system_coredns-787d4945fb-tqqzv_97ba3afd-9a66-4645-a06a-98cefa6c3fdb
kube-system_etcd-minikube_a121e106627e5c6efa9ba48006cc43bf
kube-system_kube-apiserver-minikube_cdcbce216c62c4407ac9a51ac013e7d7
kube-system_kube-controller-manager-minikube_466b9e73e627277a8c24637c2fa6442d
kube-system_kube-proxy-hgcl9_93dd26f8-fff4-4ad0-bd45-c99e9390ef10
kube-system_kube-scheduler-minikube_0818f4b1a57de9c3f9c82667e7fcc870
kube-system_storage-provisioner_ba75e191-29a6-4f6d-b1ce-f007c4eb28f2
kubernetes-dashboard_dashboard-metrics-scraper-5c6664855-psplc_a5ed6ff1-60db-4210-97ae-1b3d28afda0a
kubernetes-dashboard_kubernetes-dashboard-55c4cbbc7c-fw9xq_577b8f49-3f79-4508-85fa-66400b432ee7
```

En resumen, un DaemonSet en Kubernetes es un controlador que garantiza la presencia de un pod en todos los nodos del clúster, lo que permite ejecutar tareas específicas en cada uno de ellos de manera automatizada.

### Storage


Un PersistentVolume (PV) en Kubernetes es un recurso que proporciona almacenamiento persistente en un clúster de Kubernetes. Es una abstracción que representa un volumen físico o un recurso de almacenamiento en la infraestructura subyacente, como un disco duro en un servidor o un volumen de red.

Un PersistentVolume se define por su capacidad de almacenamiento, acceso y modo de reclamación. La capacidad de almacenamiento indica la cantidad de datos que se pueden almacenar en el volumen. El acceso se refiere a cómo los pods pueden acceder al volumen, ya sea de forma exclusiva (acceso de lectura-escritura) o compartida (acceso de solo lectura). El modo de reclamación define cómo se asigna y libera el volumen.

Los PersistentVolumes se crean de forma independiente de los pods y los nombres de los volúmenes no están directamente vinculados a ningún pod en particular. En su lugar, los pods pueden reclamar y utilizar los PersistentVolumes mediante PersistentVolumeClaims (PVC). Un PVC especifica los requisitos de almacenamiento que necesita un pod y solicita un PersistentVolume compatible que cumpla con esos requisitos.

En la máquina donde está corriendo el minikube, crear el folder del PV:


``` bash
mkdir -p /tmp/minikube/pv1
```


Creamos el archivo `pv.yaml`
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: minikube-pv
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /tmp/minikube/pv1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - minikube
```

Declarándolo y viendo su creación:

``` bash
fede@lincon:~$ kubectl apply -f pv.yaml
persistentvolume/minikube-pv created
fede@lincon:~$ kubectl get pv
NAME          CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS    REASON   AGE
minikube-pv   1Gi        RWO            Delete           Available           local-storage            8s
```

Cuando un PersistentVolumeClaim se realiza, Kubernetes encuentra un PersistentVolume disponible que cumpla con los requisitos y lo enlaza al PVC. A continuación, el PVC se puede montar en los pods que lo soliciten, proporcionándoles almacenamiento persistente. Esto permite que los datos se conserven incluso si los pods se eliminan o reinician.

Creamos el archivo `stateful.yaml`
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: local-storage
      resources:
        requests:
          storage: 1Gi
```

Aplicando este último archivo:

``` bash
fede@lincon:~$ kubectl apply -f stateful.yaml
statefulset.apps/web configured
fede@lincon:~$ kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
web-0   1/1     Running   0          3s
web-1   0/1     Pending   0          2s
fede@lincon:~$ kubectl get pvc
NAME        STATUS    VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS    AGE
www-web-0   Bound     minikube-pv   1Gi        RWO            local-storage   4m55s
www-web-1   Pending                                           local-storage   17s
```

Se puede ver que uno de los PVC logró hacer binding con el PV pero el otro no encontró candidato, y por lo tanto el pod no pueden ser creado, ya que su dependencia no está disponible.

## Helm

Para instalar helm en linux: [Fuente](https://helm.sh/docs/intro/install/)


``` bash
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Una vez instalado, vamos a instalar un chart desarrollado por un tercero, Bitnami en este caso. Instalamos el repositorio de Bitnami:

``` bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Y ahora a instalar un chart. Para eso vamos a crear un namespace nuevo y confirmar si creación.

```bash
fede@lincon:~$ k create ns metrics
namespace/metrics created
fede@lincon:~$ kg ns
NAME                   STATUS   AGE
default                Active   10d
fede-ns                Active   8d
kube-node-lease        Active   10d
kube-public            Active   10d
kube-system            Active   10d
kubernetes-dashboard   Active   10d
metrics                Active   7s
```

Con el namespace creado, desplegamos el chart:

```bash
fede@lincon:~$ helm install kube-state-metrics bitnami/kube-state-metrics -n metrics
NAME: kube-state-metrics
LAST DEPLOYED: Mon Jun 12 18:05:20 2023
NAMESPACE: metrics
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kube-state-metrics
CHART VERSION: 3.5.4
APP VERSION: 2.9.2

** Please be patient while the chart is being deployed **

Watch the kube-state-metrics Deployment status using the command:

    kubectl get deploy -w --namespace metrics kube-state-metrics

kube-state-metrics can be accessed via port "8080" on the following DNS name from within your cluster:

    kube-state-metrics.metrics.svc.cluster.local

To access kube-state-metrics from outside the cluster execute the following commands:

    echo "URL: http://127.0.0.1:9100/"
    kubectl port-forward --namespace metrics svc/kube-state-metrics 9100:8080
```

Conectándose al puerto 9100 podemos ver todas las métricas generadas.

Y con los siguientes comandos podemos inspeccionar los objetos desplegados:

``` bash
fede@lincon:~$ kg all -n metrics
NAME                                     READY   STATUS    RESTARTS   AGE
pod/kube-state-metrics-769d5c456-7bpmw   1/1     Running   0          18m

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kube-state-metrics   ClusterIP   10.107.94.210   <none>        8080/TCP   18m

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kube-state-metrics   1/1     1            1           18m

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/kube-state-metrics-769d5c456   1         1         1       18m
```

También podemos explorar el chart y sus definiciones: 

``` bash
fede@lincon:~$ helm show chart bitnami/kube-state-metrics
annotations:
  category: Analytics
  licenses: Apache-2.0
apiVersion: v2
appVersion: 2.9.2
dependencies:
- name: common
  repository: oci://registry-1.docker.io/bitnamicharts
  tags:
  - bitnami-common
  version: 2.x.x
description: kube-state-metrics is a simple service that listens to the Kubernetes
  API server and generates metrics about the state of the objects.
home: https://bitnami.com
icon: https://bitnami.com/assets/stacks/kube-state-metrics/img/kube-state-metrics-stack-220x234.png
keywords:
- prometheus
- kube-state-metrics
- monitoring
maintainers:
- name: VMware, Inc.
  url: https://github.com/bitnami/charts
name: kube-state-metrics
sources:
- https://github.com/bitnami/charts/tree/main/bitnami/kube-state-metrics
version: 3.5.4
```

Para ver los valores de configuración usados en el despliegue, se puede hacer: 

``` bash
fede@lincon:~$ helm show values bitnami/kube-state-metrics > values.yaml
```

El outout, almacenado en values.yaml, corresponde a todos los valores configurables dentro del chart. Se pueden customizar y volver a aplicar. 

Para ver la versión de char podemos hacer:

```bash
fede@lincon:~$ helm ls -n metrics
NAME              	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART                   	APP VERSION
kube-state-metrics	metrics  	1       	2023-06-12 18:05:20.165548026 +0000 UTC	deployed	kube-state-metrics-3.5.4	2.9.2
```

En mi output, el chart tiene una versión 3.5.4 y corresponde a la versión del chart, no del código de la aplicación. La aplicación, el código de la misma, corresponde al release 2.9.2.