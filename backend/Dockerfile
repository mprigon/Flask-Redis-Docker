FROM redis:alpine

WORKDIR .
# COPY dump.rdb .

EXPOSE "6379"
# CMD redis-server
# redis-server will start in docker-compose.yml with redis.conf
# services - redis - command

# контейнер не обрабатывал сигнал SIGTERM, пока не задал в
# Dockerfile ENTRYPOINT. Если перенести в
# Dockercompose, то при docker compose stop 10 секунд ждет,
# а потом SIGKILL , без сохранения dump.rdb
RUN mkdir -p /usr/local/etc/redis
COPY <<EOF /usr/local/etc/redis/redis.conf
bind 0.0.0.0
save 900 1
save 300 10
save 60 10000
shutdown-on-sigint default
shutdown-on-sigterm default
dbfilename dump.rdb
EOF

ENTRYPOINT ["redis-server", "/usr/local/etc/redis/redis.conf"]
