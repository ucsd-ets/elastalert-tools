FROM wuykimpang/centos8-extended:latest

COPY . /opt/elastalert-handler

RUN pip3 install tox pytest

# install project
RUN cd /opt/elastalert-handler && \
    python3 setup.py bdist_wheel && \
    pip3 install dist/*.whl

COPY ./config /home/kube/.kube/config

WORKDIR /opt/elastalert-handler

ENV JUPYTERHUB_BASEURL='https://datahub.ucsd.edu'
ENV JUPYTERHUB_API_TOKEN='SOMETHING'