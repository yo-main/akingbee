#!/bin/sh

rm /etc/nginx/htpasswd.users
echo -n $NGINX_AUTH_USERNAME: >> /etc/nginx/htpasswd.users
echo $NGINX_AUTH_PWD >> /etc/nginx/htpasswd.users

nginx -g 'daemon off;'
