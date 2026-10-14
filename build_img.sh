server_name=$(basename "$(dirname "$0")")
docker rmi $server_name:latest
docker build -f Dockerfile -t $server_name:latest .
