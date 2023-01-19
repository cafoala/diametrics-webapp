# Build and deploy with GitHub Actions

The action defined in ```azure-container-webapp.yml``` is in two parts - build, and deploy.

Note - this application uses a single container. More complex applications can use multiple containers, but would require a different deployment technique, e.g. Kubernetes. 

## Build

In 'build' the application is packaged into a container using ```docker build``` and the container definition in Dockerfile.
The code to be deployed,  dependencies, evnvironment, and how the program is launched are all defined in the Dockerfile.

Once the Docker container has been built, it needs to be saved somewhere so it can be deployed. Typically containers are saved (or 'pushed') to a container 'registry'.  We are using https://ghcr.io also known as GitHub packages.
 
The build part of the action enables ```packages: write``` and uses the predefined ```secrets.GITHUB_TOKEN``` to log in to ghcr.io.  If you use a different regisry you will need to provide a username and password.

Note - if your repository is private, your packages, including containers, will also be private, so authentication will be required to access them.

## Deploy

Deployment is quite simple, but requires authentication, so it can easily go wrong.  Notably the GitHub action can show success, but the new container is not running on Azure because it couldn't be pulled from the registry.

### Create Azure Web App

In the Azure Portal https://portal.azure.com/ create a new App Service.  Select 'Docker Container' for the 'Publish' option.

Accept the default values and create the app.  It takes a couple of minutes.  Check that you can access the sample web site.

### Application settings

To enable the web app to fetch your Docker container from ghcr.io the the registry password, url, and username must be entered in the Application Settings, these can be found in 'Settings' -> 'Configuration' in the App Services settings for your App Service.


```
DOCKER_REGISTRY_SERVER_PASSWORD  = ghp_....
DOCKER_REGISTRY_SERVER_URL = https://ghcr.io
DOCKER_REGISTRY_SERVER_USERNAME = <YOUR GITHUB USERNAME>
WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
```

Note that the password is NOT you GitHub or Azure password.  The password required here is a GitHub 'classic' token with the permission 'read:packages'.
This token is generated in the ```< > Developer settings``` page on the GitHub website. 
For full details see https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry


### Publish profile

The GitHub action requires a  


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