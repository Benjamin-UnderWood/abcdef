import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
# r.hdel("notice", "wx1047894")
dic = r.hget("notice", "wx1047894")
print(dic)
