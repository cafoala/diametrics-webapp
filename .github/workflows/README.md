# Build and deploy with GitHub Actions




## Local build and run of Docker container

This is optional, and requires a Docker desktop is installed.

Build Docker container image using the ```Dockerfile``` in the current directory (.) and tag in with the name ```diametrics-webapp-dash```.

```sh
docker build -t diametrics-webapp-dash:latest .
```

Run the docker container

```sh
docker run -p 5050:80 diametrics-webapp-dash
```