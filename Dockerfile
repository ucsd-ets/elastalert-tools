# used for development purposes
FROM wuykimpang/centos8-extended:latest

COPY . /opt/elastalert-tools

RUN pip3 install tox pytest

RUN mkdir /var/lib/elastalert-tools

# install project
RUN cd /opt/elastalert-tools && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

#COPY ./config /home/kube/.kube/config

WORKDIR /opt/elastalert-tools

# supply these to build arg --build-arg JUPYTERHUB_API_TOKEN=...
ARG JUPYTERHUB_API_TOKEN
ARG LIVE_DATAHUB_TEST

ENV JUPYTERHUB_BASEURL='https://datahub-dev.ucsd.edu/hub/api/'

ENV JUPYTERHUB_API_TOKEN=${JUPYTERHUB_API_TOKEN}
ENV LIVE_DATAHUB_TEST=${LIVE_DATAHUB_TEST}