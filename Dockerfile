# Custom jupyterhub image to install the needed dockerspawner package.
# Everything else should directly come from the base image jupyterhub/jupyterhub

ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install additional packages here
RUN python3 -m pip install --no-cache-dir \
    dockerspawner

# In the future, install common packages used by students / team members here

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
