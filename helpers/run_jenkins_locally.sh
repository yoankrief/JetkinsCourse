docker run --name jenkins-blueocean -u root --rm -d -p 8080:8080 -v jenkins-data:/var/jenkins_home \
-v /var/run/docker.sock:/var/run/docker.sock jenkinsci/blueocean

# NOTES

# --name  Gives a name to the running container
# --rm  Automatically removes the Docker container when it is shut down.
# -d    Runs the jenkinsci/blueocean container in the background ("detached" mode)
# -p    Makes (i.e. "publishes") port 8080 of the jenkinsci/blueocean container to port 8080 on the
#       host machine. The 1st number represents the port on the host while the 2nd represents the
#       container’s port.
# -v    Maps the /var/jenkins_home directory in the container to the Docker volume with the name
#       jenkins-data. If this volume does not exist, then this docker run command will automatically
#       create the volume for you.

# Note about /var/run/docker.sock:/var/run/docker.sock:
# This mounting basically exposes the host docker daemon to the container.
# so you can invoke docker api/client from WITHIN your container, to start/stop/build images/containers like directly calling those commands on the host.
