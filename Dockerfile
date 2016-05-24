FROM mhoush/py3


COPY . /app


RUN apk add --no-cache openssl && \
    pip install --upgrade --no-cache-dir \
    devpi-client \
    sphinx \
    setuptools \
    -e /app && \
    rm -rf /var/tmp/* /tmp/* /root/.cache/ /var/cache/apk/*

VOLUME /app
VOLUME /config
VOLUME /certs

WORKDIR /app

CMD "sh"
