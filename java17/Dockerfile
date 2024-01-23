FROM openjdk:17-slim

LABEL org.opencontainers.image.source=https://github.com/rszewczyk2204/docker-images

COPY ../java_files/* /usr/local/bin

RUN apt-get update \
    && apt-get -y --no-install-recommends install docker.io \
        git \
        make \
        moreutils \
        python3 \
        python3-pip \
        ssh \
        curl \
        maven \
        gradle \
    && apt-get -y purge --auto-remove \
    && pip3 install --no-cache-dir anybadge \
    && GFJ=1.19.1 && curl --location --fail "https://github.com/google/google-java-format/releases/download/v${GFJ}/google-java-format-${GFJ}-all-deps.jar" -o /opt/google-java-format.jar \
    && apt-get -y clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp*