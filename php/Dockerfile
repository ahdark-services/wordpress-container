ARG PHP_VERSION=8.0
FROM php:${PHP_VERSION}-fpm

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

# Download WordPress
ARG WORDPRESS_VERSION=latest
RUN curl -o /tmp/wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz"
RUN tar -xzf /tmp/wordpress.tar.gz -C /var/www/html --strip-components=1
RUN rm -f /tmp/wordpress.tar.gz
RUN chmod -R 755 /var/www/html
RUN chown -R www-data:www-data /var/www/html

EXPOSE 9000

WORKDIR /var/www/html

ENTRYPOINT ["php-fpm", "-F"]
