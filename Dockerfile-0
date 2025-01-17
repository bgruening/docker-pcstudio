FROM jlesage/baseimage-gui:ubuntu-24.04-v4 AS build

MAINTAINER Bjoern Gruening, bjoern.gruening@gmail.com

RUN apt-get update -y && \
     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         ca-certificates \
         wget \
         libgl1 \
         xz-utils \
         openjfx \
         nano \
         qt5dxcb-plugin && \
     rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/qupath &&\
    chmod 777 /opt/qupath &&\
    cd /opt/qupath/ && \
    wget https://github.com/qupath/qupath/releases/download/v0.5.1/QuPath-v0.5.1-Linux.tar.xz &&\
    tar -xvf QuPath-v0.5.1-Linux.tar.xz && \
    mv /opt/qupath/QuPath-v0.5.1-Linux/* /opt/qupath/ && \
    rm /opt/qupath/QuPath-v0.5.1-Linux.tar.xz /opt/qupath/QuPath-v0.5.1-Linux/ -rf && \
    chmod u+x /opt/qupath/QuPath/bin/QuPath

# Generate and install favicons.
RUN APP_ICON_URL=https://github.com/qupath/qupath/wiki/images/qupath_128.png && \
    install_app_icon.sh "$APP_ICON_URL"

COPY startapp.sh /startapp.sh
RUN chmod +x /startapp.sh

# Installing a few extensions
RUN cd /opt/qupath/QuPath/lib/app/ && \
    wget https://github.com/qupath/qupath-extension-djl/releases/download/v0.3.0/qupath-extension-djl-0.3.0.jar &&\
    wget https://github.com/qupath/qupath-extension-stardist/releases/download/v0.5.0/qupath-extension-stardist-0.5.0.jar &&\
    sed -i '/^\[Application\]$/a app.classpath=$APPDIR/qupath-extension-djl-0.3.0.jar' QuPath.cfg  && \
    sed -i '/^\[Application\]$/a app.classpath=$APPDIR/qupath-extension-stardist-0.5.0.jar' QuPath.cfg

# Set the name of the application.
ENV APP_NAME="QuPath"

ENV KEEP_APP_RUNNING=0

ENV TAKE_CONFIG_OWNERSHIP=1

COPY rc.xml.template /opt/base/etc/openbox/rc.xml.template

WORKDIR /config
