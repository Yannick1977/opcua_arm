# commande pour build l'image

docker buildx build --platform linux/arm/v7 -t opcua-arm . --output type=docker

# commande pour recuperer une image en specifiant une image
docker pull --platform linux/arm/v7 arm32v7/python 

<....> to replace

# Docker Tag & Save: 
docker tag <342c3922c759>  portainer save --output <portainer.tar> <342c3922c759>

# Docker Load:
docker -H <172.16.12.1> load --input <portainer.tar>



# lien docs asyncopcua
https://opcua-asyncio.readthedocs.io/en/latest/usage/common/node-nodeid.html
