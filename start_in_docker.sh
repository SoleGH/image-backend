
server_name=$(basename "$(dirname "$0")")
docker stop $server_name
docker rm $server_name
docker run -d -v "$(pwd)/src":/src -v "$(pwd)/../${server_name}_conf.json":/src/onf.json -w /src -p 5000:5000 --sysctl net.ipv6.conf.all.disable_ipv6=0 --sysctl net.ipv6.conf.default.disable_ipv6=0 --name $server_name $server_name:latest bash -c "flask db upgrade && python app.py"

