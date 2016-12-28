import redis, time
import json


def main():
    pool = redis.ConnectionPool(host='139.199.65.115', port=6379, db=0,password='melodicdeath')
    r = redis.Redis(connection_pool=pool)
    # while 1:
    #     result = r.brpop('order_platform:phone_charge:order', 5)
    #     if result:
    #         print result
    #         print r.hgetall('order_platform:phone_charge:trade_no:%s' % result[1])
    r.hmset('11111', {'1': '1'})
    print r.hgetall('11111')
    r.delete('11111')
    print r.hgetall('11111')
    # print r.hgetall('order_platform:phone_charge:trade_no:20161210144757362LUDNA00027')
    # print r.hdel('order_platform:phone_charge:trade_no:20161210144757362LUDNA00027')


if __name__ == "__main__":
    main()
