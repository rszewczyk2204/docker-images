FROM python:3

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

LABEL org.opencontainers.image.source=https://github.com/rszewczyk2204/docker-images

COPY python/*.py /usr/bin

RUN git clone --depth=1 https://github.com/sourcegraph/lsif-py /opt/lsif-py \
    && cd /opt/lsif-py \
    && pip install --no-cache-dir jedi==0.17.2 \
    && pip install anybadge \
    && pip install python-gitlab \
    && pip install black \
    && pip install --upgrade pyyaml==6.0.1 \
    && pip install --no-cache-dir --upgrade poetry \
    && apt-get update \
    && apt-get install --yes --no-install-recommends docker.io \
	cython3 \
	mypy \
    && apt-get clean autoclean --yes \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{cache,log}/ \
    && rm -rf /tmp/*
