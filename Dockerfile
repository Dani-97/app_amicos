FROM ubuntu:25.04

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd" \
    APP_DIR="${HOME_DIR}/app" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev nano -y

ENV PYTHON_VERSION="3.11.5"
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
RUN tar -xf Python-${PYTHON_VERSION}.tgz
WORKDIR ./Python-${PYTHON_VERSION}
RUN ./configure --enable-optimizations
RUN make -j 12
RUN make altinstall

# system requirements to build most of the recipes
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq --yes --no-install-recommends \
    autoconf \
    automake \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libssl-dev \
    libtool \
    openjdk-17-jdk \
    patch \
    pkg-config \
    sudo \
    unzip \
    zip \
    zlib1g-dev

# # prepares non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${APP_DIR}
RUN sudo chown user:user ${APP_DIR}
COPY --chown=user:user . ${APP_DIR}

RUN alias python=python3.11
RUN alias python3=python3.11
RUN alias pip="python3.11 -m pip"
RUN alias pip3="python3.11 -m pip"

WORKDIR ${APP_DIR}/src
COPY --chown=user:user ./src ${APP_DIR}/src
RUN sudo ln -s /usr/local/bin/python3.11 /usr/local/bin/python3
RUN sudo ln -s /usr/local/bin/python3.11 /usr/local/bin/python

# # installs buildozer and dependencies
RUN python3 -m pip install -r requirements.txt

# RUN yes | bash create_debug_apk.sh
