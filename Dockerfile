#
# CatchEmAll Dockerfile
#
# https://github.com/0ssigeno/CatchEmAll
#

FROM ubuntu:latest



ARG MARIADB_KEY_URL='https://mariadb.org/mariadb_release_signing_key.asc'
ARG MARIADB_APT_REPO='deb [arch=amd64,arm64,ppc64el] http://ftp.nluug.nl/db/mariadb/repo/10.4/ubuntu bionic main' 


#DEFAULT VALUE FOR BUILD SUCCESS
ARG TOR_PWD='PLEASECHANGEME'
ARG TOR_KEY_URL='https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc'
ARG TOR_APT_REPO='deb  https://deb.torproject.org/torproject.org bionic main'


# Install MariaDB
RUN \
  apt-get update && \
  apt-get install -y software-properties-common && \
  apt-key adv --fetch-keys "$MARIADB_KEY_URL" && \
  add-apt-repository "$MARIADB_APT_REPO" && \
  apt-get update && \
  apt-get install -y mariadb-server default-libmysqlclient-dev && \
  sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/my.cnf && \
  echo "mysqld_safe &" > /tmp/config && \
  echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
  echo "mysql -e 'CREATE USER \"root\"@\"%\"; GRANT ALL PRIVILEGES ON *.* TO \"root\"@\"%\" WITH GRANT OPTION; FLUSH PRIVILEGES;'" >> /tmp/config && \
  bash /tmp/config && \
  rm -f /tmp/config


# Install Tor
RUN \
  apt-key adv --fetch-keys "$TOR_KEY_URL" && \
  add-apt-repository "$TOR_APT_REPO" && \
  apt-get update && \
  apt-get install -y tor deb.torproject.org-keyring && \
  echo "CookieAuthentication 1\nCookieAuthFile /var/lib/tor/control_auth_cookie\nCookieAuthFileGroupReadable 1\nDataDirectoryGroupReadable 1" >>/etc/tor/torrc  && \
  echo "HashedControlPassword $(tor --hash-password ${TOR_PWD} | sed '2q;d')" >> /etc/tor/torrc && \
  echo "ControlSocket /var/lib/tor/control_socket\nControlSocketsGroupWritable 1\nDataDirectoryGroupReadable 1\nCacheDirectoryGroupReadable 1" >> /etc/tor/torrc&& \
  echo "ControlPort 9051" >> /etc/tor/torrc && \
  service tor start

RUN \
    apt-get install -y python3 python3-pip python-dev git

RUN \
    git clone -b develop https://github.com/0ssigeno/CatchEmAll \
    && cd CatchEmAll \
    && pip3 install -r requirements.txt \
    && python3 setup.py install \
    && rm -rf /tmp/*




# Define mountable directories.
# VOLUME ["/etc/mysql", "/var/lib/mysql"]

# Define working directory.
WORKDIR /CatchEmAll

ENV HOME /CatchEmAll

CMD bash

