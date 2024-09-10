ARG PHP_VERSION=8.0
FROM php:${PHP_VERSION}-fpm

# Install dependencies
RUN apt update && apt upgrade -y

# Install supervisor
RUN apt install -y supervisor

# Install PHP extensions
ADD --chmod=0755 https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/
ARG PHP_EXTENSIONS="gd opcache zip pdo_mysql mysqli redis xdebug imagick exif mbstring zip"
RUN install-php-extensions ${PHP_EXTENSIONS}

RUN echo "opcache.enable=1" >> /usr/local/etc/php/conf.d/opcache.ini
RUN echo "opcache.enable_cli=1" >> /usr/local/etc/php/conf.d/opcache.ini
RUN echo "opcache.memory_consumption=256" >> /usr/local/etc/php/conf.d/opcache.ini
RUN echo "memory_limit=2048M" >> /usr/local/etc/php/conf.d/performance.ini
RUN echo "upload_max_filesize=100M" >> /usr/local/etc/php/conf.d/performance.ini
RUN echo "post_max_size=100M" >> /usr/local/etc/php/conf.d/performance.ini

COPY supervisor/php-fpm.conf /etc/supervisor/conf.d/php-fpm.conf

# Install nginx
RUN apt update && apt install -y gnupg2 ca-certificates lsb-release debian-archive-keyring \
    && curl -fsSL https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
    http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | tee /etc/apt/sources.list.d/nginx.list \
    && apt update

RUN apt install -y nginx

# Clean up APT cache to reduce image size
RUN apt clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/nginx/snippets
COPY fastcgi-php.conf /etc/nginx/snippets/fastcgi-php.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

# Download WordPress
ARG WORDPRESS_VERSION=latest
RUN curl -o /tmp/wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz"
RUN tar -xzf /tmp/wordpress.tar.gz -C /var/www/html --strip-components=1
RUN rm -f /tmp/wordpress.tar.gz
RUN chmod -R 755 /var/www/html
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

WORKDIR /var/www/html

ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
