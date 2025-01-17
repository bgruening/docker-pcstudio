FROM jlesage/baseimage-gui:ubuntu-24.04-v4 AS build

MAINTAINER Randy Heiland, randy.heiland@gmail.com

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

RUN mkdir -p /opt/pcstudio &&\
    chmod 777 /opt/pcstudio &&\
    cd /opt/pcstudio/ && \
    wget https://github.com/pcstudio/pcstudio/releases/download/v0.5.1/pcstudio-v0.5.1-Linux.tar.xz &&\
    tar -xvf pcstudio-v0.5.1-Linux.tar.xz && \
    mv /opt/pcstudio/pcstudio-v0.5.1-Linux/* /opt/pcstudio/ && \
    rm /opt/pcstudio/pcstudio-v0.5.1-Linux.tar.xz /opt/pcstudio/pcstudio-v0.5.1-Linux/ -rf && \
    chmod u+x /opt/pcstudio/pcstudio/bin/pcstudio

# Generate and install favicons.
RUN APP_ICON_URL=https://github.com/pcstudio/pcstudio/wiki/images/pcstudio_128.png && \
    install_app_icon.sh "$APP_ICON_URL"

COPY startapp.sh /startapp.sh
RUN chmod +x /startapp.sh

# Installing a few extensions
RUN cd /opt/pcstudio/pcstudio/lib/app/ && \
    wget https://github.com/pcstudio/pcstudio-extension-djl/releases/download/v0.3.0/pcstudio-extension-djl-0.3.0.jar &&\
    wget https://github.com/pcstudio/pcstudio-extension-stardist/releases/download/v0.5.0/pcstudio-extension-stardist-0.5.0.jar &&\
    sed -i '/^\[Application\]$/a app.classpath=$APPDIR/pcstudio-extension-djl-0.3.0.jar' pcstudio.cfg  && \
    sed -i '/^\[Application\]$/a app.classpath=$APPDIR/pcstudio-extension-stardist-0.5.0.jar' pcstudio.cfg

# Set the name of the application.
ENV APP_NAME="pcstudio"

ENV KEEP_APP_RUNNING=0

ENV TAKE_CONFIG_OWNERSHIP=1

COPY rc.xml.template /opt/base/etc/openbox/rc.xml.template

WORKDIR /config
