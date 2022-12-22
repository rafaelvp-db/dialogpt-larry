# import config.
# You can change the default config with `make cnf="config_special.env" build`
cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help frontend backend

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help	

network:
	docker network rm tmpnetwork -f && \
	docker network create --driver bridge tmpnetwork

run:
	docker compose stop && docker container prune --force && docker image prune --force && docker compose up

frontend:
	docker build -t ${APP_NAME}/frontend:1.0 ./frontend

backend:
	docker build -t ${APP_NAME}/backend:1.1 ./backend

run-frontend:
	docker run -it --name frontend --net tmpnetwork --rm -p 8080:80 ${APP_NAME}/frontend:latest

run-backend:
	docker run -it --name backend --net tmpnetwork --rm -p 8000:8080 --env-file=.env ${APP_NAME}/backend:1.1

stop:
	docker compose stop

deploy:
	helm upgrade --install --namespace larry --create-namespace larry $$(pwd)/helm/larry/

remove:
	kubectl delete ns larry

forward:
	nohup kubectl port-forward svc/larry -n larry 8000:8000 &

tfclean:
	rm -rf ./terraform .terraform && rm -rf terraform.lock.hcl && rm -rf terraform.tfstate && rm -rf terraform.tfstate.backup

aks-install-cli:
	az aks install-cli
	
aks-login:
	bash -c "az aks get-credentials --resource-group ${RESOURCE_GROUP_NAME} --name ${AKS_CLUSTER_NAME}"

test:
	source test/.venv/bin/activate && python ./test/test_aks.py