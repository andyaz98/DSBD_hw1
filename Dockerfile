FROM mysql:5.6

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=hw1
ENV MYSQL_USER=andrea
ENV MYSQL_PASSWORD=password


VOLUME /var/lib/mysql
EXPOSE 3306


