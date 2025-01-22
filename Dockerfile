# FROM ubuntu:22.04
FROM jlesage/baseimage-gui:ubuntu-24.04-v4 AS build

# MAINTAINER Randy Heiland, randy.heiland@gmail.com

ENV DEBIAN_FRONTEND=noninteractive

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

ENV DISPLAY=:0

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
         ca-certificates \
         wget \
         libgl1 \
         xz-utils \
         openjfx \
         nano \
         qt5dxcb-plugin \
         python3-full python3-pyqt5 python3-pyqt5.qtsvg python3-pip
#     rm -rf /var/lib/apt/lists/*

# RUN pip install numpy matplotlib scipy pandas
# RUN python3 -m pip install numpy matplotlib scipy pandas
# RUN python3 -m venv /tmp/my-venv
# RUN ls /tmp/my-venv
# RUN /tmp/my-venv/bin/pip install numpy matplotlib scipy pandas
RUN python3 -m venv /usr/local/pcstudio-venv
#RUN /usr/local/pcstudio-venv/bin/pip install numpy matplotlib scipy pandas
RUN /usr/local/pcstudio-venv/bin/pip install PyQt5 matplotlib scipy pandas


RUN mkdir -p /opt/pcstudio/bin/images &&\
    mkdir -p /opt/pcstudio/bin/icon &&\
    mkdir -p /opt/pcstudio/config &&\
    chmod -R 777 /opt/pcstudio 

# Generate and install favicons.
# RUN APP_ICON_URL=https://github.com/pcstudio/pcstudio/wiki/images/pcstudio_131.png && \
#     install_app_icon.sh "$APP_ICON_URL"

# COPY startapp.sh /startapp.sh
# RUN chmod +x /startapp.sh

COPY ./bin/* /opt/pcstudio/bin/
COPY ./bin/images/* /opt/pcstudio/bin/images/
COPY ./bin/icon/* /opt/pcstudio/bin/icon/
COPY ./config/* /opt/pcstudio/config/

# Installing a few extensions
# RUN cd /opt/pcstudio/pcstudio/lib/app/ && \
#     wget https://github.com/pcstudio/pcstudio-extension-djl/releases/download/v0.3.0/pcstudio-extension-djl-0.3.0.jar &&\
#     wget https://github.com/pcstudio/pcstudio-extension-stardist/releases/download/v0.5.0/pcstudio-extension-stardist-0.5.0.jar &&\
#     sed -i '/^\[Application\]$/a app.classpath=$APPDIR/pcstudio-extension-djl-0.3.0.jar' pcstudio.cfg  && \
#     sed -i '/^\[Application\]$/a app.classpath=$APPDIR/pcstudio-extension-stardist-0.5.0.jar' pcstudio.cfg

# Set the name of the application.
ENV APP_NAME="pcstudio"

ENV KEEP_APP_RUNNING=0

ENV TAKE_CONFIG_OWNERSHIP=1

COPY rc.xml.template /opt/base/etc/openbox/rc.xml.template

WORKDIR /config
