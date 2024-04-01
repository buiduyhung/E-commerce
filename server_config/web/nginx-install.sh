#!/bin/bash

set -euxo pipefail

NGINX_VERSION="1.25.1"
VOD_MODULE_VERSION="1.31"
SECURE_TOKEN_MODULE_VERSION="1.5"
RTMP_MODULE_VERSION="1.2.2"

cp /etc/apt/sources.list /etc/apt/sources.list.d/sources-src.list
sed -i 's|deb http|deb-src http|g' /etc/apt/sources.list.d/sources-src.list
apt-get update

apt-get -yqq build-dep nginx

apt-get -yqq install --no-install-recommends ca-certificates wget
update-ca-certificates -f


mkdir /tmp/nginx
wget -nv https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
tar -zxf nginx-${NGINX_VERSION}.tar.gz -C /tmp/nginx --strip-components=1
rm nginx-${NGINX_VERSION}.tar.gz
mkdir /tmp/nginx-vod-module
wget -nv https://github.com/kaltura/nginx-vod-module/archive/refs/tags/${VOD_MODULE_VERSION}.tar.gz
tar -zxf ${VOD_MODULE_VERSION}.tar.gz -C /tmp/nginx-vod-module --strip-components=1
rm ${VOD_MODULE_VERSION}.tar.gz

cd /tmp/nginx

./configure --prefix=/etc/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/run/nginx.pid \
    --sbin-path=/usr/sbin/nginx \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-threads \
    --with-stream \
    --with-cc-opt="-O3 -Wno-error=implicit-fallthrough" \
    --add-module=../nginx-vod-module

make && make install
# rm -rf /usr/local/nginx/html /usr/local/nginx/conf/*.default

    # --with-file-aio \