FROM ghcr.io/home-assistant/base:3.23

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV LANG=C.UTF-8

RUN apk update && \
    apk add --no-cache \
        iw \
        hostapd \
        networkmanager \
        networkmanager-cli \
        net-tools \
        sudo \
        jq \
        dnsmasq \
        iptables && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /www/cgi-bin /var/lib/misc

COPY hostapd.conf /
COPY dnsmasq.conf /
COPY index.html /www/
COPY leases.cgi /www/cgi-bin/index.cgi

COPY run.sh /
RUN chmod a+x /run.sh /www/cgi-bin/index.cgi

CMD [ "/run.sh" ]
