docker image prune -f

DOCKER_BUILDKIT=1 docker build -f Dockerfile.pg -t gong-fastapi-backend:latest .

docker images

