docker run --name redis-stack \
    -d \
    -p 127.0.0.1:8001:8001 \
    -p 127.0.0.1:6379:6379 \
    redis/redis-stack:6.2.6-v10
