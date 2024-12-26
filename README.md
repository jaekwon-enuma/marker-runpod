# Build the Docker image
docker build -t ghcr.io/jaekwon-enuma/marker-server:latest .

# Push it to GitHub Container Registry
# First, login to ghcr.io (you'll need a GitHub Personal Access Token with packages:write permission)
export GH_PAT=xxxx
echo $GH_PAT | docker login ghcr.io -u jaekwon-enuma --password-stdin

# Push the image
docker push ghcr.io/jaekwon-enuma/marker-server:latest
