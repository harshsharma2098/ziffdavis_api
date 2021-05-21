### Run following command in docker setting
docker network create genietalknetwork

### Create universal tfserving container with name as "universal-tfserving-service"
docker run --network=genietalknetwork -d -p 8501:8501 --name universal-tfserving-service genietalk/universal_tfserving:4.0

### Build docker images of respective apps 
docker build -t genietalk/flask_nginx:1.0 .
docker build -t genietalk/flask_app:1.0 .

### Push images on docker hub
docker login
docker push genietalk/flask_nginx:1.0
docker push genietalk/flask_app:1.0

### Create container with name as "flask-app-service"
docker run --env UNIVERSAL_TFSERVING='http://universal-tfserving-service:8501/v1/models/universal:predict' --network=genietalknetwork -d --name flask-app-service genietalk/flask_app:1.0

### Create container with name as "flask-nginx-service"
docker run -p 80:80 --network=genietalknetwork -d --name flask-nginx-service genietalk/flask_nginx:1.0
