# used for development purposes
FROM wuykimpang/centos8-extended:latest

COPY . /opt/elastalert-tools

RUN pip3 install tox pytest

RUN mkdir /var/lib/elastalert-tools

# install project
RUN cd /opt/elastalert-tools && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

COPY ./config /home/kube/.kube/config

WORKDIR /opt/elastalert-tools

ENV JUPYTERHUB_BASEURL='https://datahub.ucsd.edu'
ENV JUPYTERHUB_API_TOKEN='SOMETHING'