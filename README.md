### Run following command in docker setting
docker network create genietalknetwork

### Build docker images of respective apps 
docker build -t genietalk/demandgen_nginx:1.0 .
docker build -t genietalk/demandgen_app:1.0 .

### Push images on docker hub
docker login
docker push genietalk/demandgen_nginx:1.0
docker push genietalk/demandgen_app:1.0

### Create container with name as "demandgen-app-service"
docker run --network=genietalknetwork -d --name demandgen-app-service genietalk/demandgen_app:1.0

### Create container with name as "demandgen-nginx-service"
docker run -p 80:80 --network=genietalknetwork -d --name demandgen-nginx-service genietalk/demandgen_nginx:1.0
