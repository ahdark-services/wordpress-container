FROM php:8.0-fpm

# Install dependencies
RUN apt update && apt upgrade -y

# Install supervisor
RUN apt install -y supervisor

# Install PHP extensions
ADD --chmod=0755 https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/
ARG PHP_EXTENSIONS="gd opcache zip pdo_mysql redis xdebug imagick exif mbstring"
RUN install-php-extensions ${PHP_EXTENSIONS}

COPY supervisor/php-fpm.conf /etc/supervisor/conf.d/php-fpm.conf

# Install nginx
COPY install-nginx.sh /tmp/install-nginx.sh
RUN chmod +x /tmp/install-nginx.sh
RUN /tmp/install-nginx.sh
RUN rm -f /tmp/install-nginx.sh

COPY default.conf /etc/nginx/conf.d/default.conf
COPY supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

# Download WordPress
ARG WORDPRESS_VERSION=latest
RUN curl -o /tmp/wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz"
RUN tar -xzf /tmp/wordpress.tar.gz -C /var/www/html --strip-components=1
RUN rm -f /tmp/wordpress.tar.gz
RUN chmod -R 755 /var/www/html
RUN chown -R www-data:www-data /var/www/html

ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
