# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # type: ignore # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
# c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.JupyterHub.spawner_class = "dockerspawner.SystemUserSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
notebook_dir = "/home/{username}"
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {
    notebook_dir: notebook_dir,  # SystemUserSpawner
    # "jupyterhub-user-{username}": notebook_dir,  # DockerSpawner
}

c.DockerSpawner.extra_create_kwargs = {
    "user": "root",  # Fix to allow /etc/group and /etc/passwd to populate with username
    "hostname": "jupyter-{username}",  # Use nice hostname instead of container ID
}

# Fix to allow Julia execution
c.DockerSpawner.extra_host_config = {"group_add": ["users"]}

# Remove containers once they are stopped?
# Removing would allow for updated images to be used when recreating
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# For the host's home directory
c.SystemUserSpawner.host_homedir_format_string = notebook_dir

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
# because we are behind a proxy, with path /jupyter/
c.JupyterHub.bind_url = "http://:8000/jupyter/"

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with PAM Authenticator
c.JupyterHub.authenticator_class = "jupyterhub.auth.PAMAuthenticator"
c.PAMAuthenticator.open_sessions = False

# Deny anyone to sign-up without approval
c.NativeAuthenticator.open_signup = False

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]

c.Authenticator.allow_all = True
c.Authenticator.delete_invalid_users = True

# Automatically create system users from jupyterhub users
c.LocalAuthenticator.create_system_users = True
