FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages and Ettercap
RUN apt-get update  \
    && apt-get -y install  \
        binutils \
        curl   \
        iproute2  \
        iputils-ping \
        nano   \
        net-tools \
        unzip \
        arping \
        conntrack \
        curl   \
        dnsutils  \
        iptables \
        mtr-tiny  \
        netcat \
        openbsd-inetd  \
        procps \
        tcpdump   \
        telnet \
        telnetd \
        asterisk \
        sipcalc \
        python3.8-distutils \
        ettercap-graphical \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY get-pip3.py /tmp
RUN python3 /tmp/get-pip3.py \
    && pip3 install scapy \
    && rm /tmp/get-pip3.py

# Create the "seed" user account
RUN useradd -m -s /bin/bash seed \
    && echo "root:dees" | chpasswd \
    && echo "seed:dees" | chpasswd
    
# Be sure to launch the asterisk server
RUN asterisk -vvv

COPY bashrc /home/seed/.bashrc
COPY bashrc /root/.bashrc
