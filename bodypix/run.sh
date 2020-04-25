image='quving/bodypix:latest'
docker pull $image
docker run --name bodypix --rm -it -p 1234:1234 $image
