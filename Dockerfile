#
# CatchEmAll Dockerfile
#
# https://github.com/0ssigeno/CatchEmAll
#

FROM ubuntu:latest

COPY . /opt/CatchEmAll

ARG MARIADB_KEY_URL='https://mariadb.org/mariadb_release_signing_key.asc'
ARG MARIADB_APT_REPO='deb [arch=amd64,arm64,ppc64el] http://ftp.nluug.nl/db/mariadb/repo/10.4/ubuntu bionic main' 


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

# Install Python and Python deps
RUN \
  apt-get install -y python3 python3-pip python-dev && \
  pip3 install -r /opt/CatchEmAll/requirements.txt && \
  rm -rf /var/lib/apt/lists/*


# Define mountable directories.
# VOLUME ["/etc/mysql", "/var/lib/mysql"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["python3", "/opt/CatchEmAll/main.py"]

# Expose ports.
#EXPOSE 3306
