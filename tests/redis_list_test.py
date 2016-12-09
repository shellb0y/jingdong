import redis, time

def handle(task):
    print task
    # time.sleep(4)

def main():
    pool = redis.ConnectionPool(host='139.199.65.115', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        result = r.brpop('trades', 4)
        print result

if __name__ == "__main__":
    main()