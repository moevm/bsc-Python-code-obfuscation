FROM ubuntu:18.04

RUN DEBIAN_FRONTEND=noninteractive apt update && apt install --no-install-recommends -y apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt install --no-install-recommends -y \
    build-essential \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel

RUN apt clean && apt-get autoremove

COPY requirements.txt /tmp
RUN pip3 --no-cache-dir install -r /tmp/requirements.txt

COPY --chown=www-data:www-data config/wsji-config.wsji /var/www/app-wsji-config.wsji
COPY --chown=www-data:www-data config/apache-config.conf /etc/apache2/sites-available/app-apache-config.conf

RUN a2dissite 000-default
RUN a2dissite default-ssl
RUN a2enmod wsgi
RUN a2ensite app-apache-config

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

EXPOSE 80

COPY --chown=www-data:www-data app /var/www/app/

ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]

