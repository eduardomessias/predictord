docker build -t predictord .
docker login
docker tag predictord eduardomessias/predictord:part2
docker push eduardomessias/predictord:part2
