# add admin role to my account
# kubectl create clusterrolebinding cluster-admin-binding \
#   --clusterrole=cluster-admin \
#   --user=$(gcloud config get-value core/account)

# set up cert-manager
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.2.0/cert-manager.yaml

# set up nginx controller
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.32.0/deploy/static/mandatory.yaml
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/provider/cloud-generic.yaml
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/do/deploy.yaml


