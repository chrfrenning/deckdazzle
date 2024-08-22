# install azure-cli
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# az login # auth yourself and select subscription
# az extension add --name containerapp --upgrade

# revision name, or use latest by default
tag=${1:-latest}

# build and push docker image
docker build -t deckdazzle .
docker tag deckdazzle $CONTAINER_REGISTRY_URL/deckdazzle:$tag
docker login $CONTAINER_REGISTRY_URL -u $CONTAINER_REGISTRY_USERNAME -p $CONTAINER_REGISTRY_PASSWORD
docker push $CONTAINER_REGISTRY_URL/deckdazzle:$tag

# create new revision of container app
az containerapp revision copy --image $CONTAINER_REGISTRY_URL/deckdazzle:$tag --revision-suffix $tag -n $CONTAINERAPP_NAME -g $CONTAINERAPP_RG