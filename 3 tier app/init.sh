kubectl create namespace webapp
kubectl create namespace database
kubectl apply -f secret-wa.yaml
kubectl apply -f secret-db.yaml

kubectl apply -f mongo-app.yaml
kubectl apply -f web-app.yaml