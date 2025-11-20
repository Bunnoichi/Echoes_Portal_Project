# nginx/Dockerfile
FROM nginx:1.25-alpine

# default.conf を Nginx の設定ディレクトリにコピー
COPY default.conf /etc/nginx/conf.d/default.conf

# static を Nginx から参照するためのディレクトリを作成（任意）
RUN mkdir -p /code/static
