ARG NGINX_VERSION=1.26.2
FROM nginx:${NGINX_VERSION}-alpine

# Install nginx
RUN mkdir -p /etc/nginx/snippets
COPY fastcgi-php.conf /etc/nginx/snippets/fastcgi-php.conf
COPY default.conf /etc/nginx/conf.d/default.conf

WORKDIR /var/www/html

# Download WordPress
ARG WORDPRESS_VERSION=latest
RUN curl -o /tmp/wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz"
RUN tar -xzf /tmp/wordpress.tar.gz -C /var/www/html --strip-components=1
RUN rm -f /tmp/wordpress.tar.gz
RUN chmod -R 755 /var/www/html
RUN chown -R nginx:nginx /var/www/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
