#!/usr/bin/python
# -*- coding:utf-8-*-
import Queue, threading, sys, os
import time

import binascii
import struct


# working thread
class Worker(threading.Thread):
    worker_count = 0

    def __init__(self, workQueue, resultQueue, timeout=0, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()

    def run(self):
        ''' the get-some-work, do-some-work main loop of worker threads '''
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                print "worker[%2d]: %s" % (self.id, str(res))
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except:
                print 'worker[%2d]' % self.id, sys.exc_info()[:2]


class WorkerManager:
    def __init__(self, num_of_workers=10, timeout=1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)

    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        print "All jobs are are completed."

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)


def test_job(id, sleep=0.001):
    try:
        result = _3ds.encrypt('中文测hel试lo wor！·*#J&^FD*mv2ld')
        result1 = _3ds.decrypt(result)
        print id, result, result1
    except:
        print '[%4d]' % id, sys.exc_info()[:2]
    return id


def test():
    import socket
    socket.setdefaulttimeout(10)
    print 'start testing'
    wm = WorkerManager(10)
    for i in range(100):
        wm.add_job(test_job, i, i * 0.001)
    wm.wait_for_complete()
    print 'end testing'


class _secret():
    """TEA 加解密, 64比特明码, 128比特密钥
这个加解密算法是MIT授权，被授权人有权利使用、复制、修改、合并、出版发行、散布、再授权及
贩售软件及软件的副本。
这是一个确认线程安全的独立加密模块，使用时必须要有一个全局变量secret_key，要求大于等于16位
    """

    def xor(self, a, b):
        op = 0xffffffffL
        a1, a2 = struct.unpack('>LL', a[0:8])
        b1, b2 = struct.unpack('>LL', b[0:8])
        return struct.pack('>LL', (a1 ^ b1) & op, (a2 ^ b2) & op)

    def code(self, v, k):
        n = 16
        op = 0xffffffffL
        delta = 0x9e3779b9L
        k = struct.unpack('>LLLL', k[0:16])
        y, z = struct.unpack('>LL', v[0:8])
        s = 0
        for i in xrange(n):
            s += delta
            y += (op & (z << 4)) + k[0] ^ z + s ^ (op & (z >> 5)) + k[1]
            y &= op
            z += (op & (y << 4)) + k[2] ^ y + s ^ (op & (y >> 5)) + k[3]
            z &= op
        r = struct.pack('>LL', y, z)
        return r

    def decipher(self, v, k):
        n = 16
        op = 0xffffffffL
        y, z = struct.unpack('>LL', v[0:8])
        a, b, c, d = struct.unpack('>LLLL', k[0:16])
        delta = 0x9E3779B9L
        s = (delta << 4) & op
        for i in xrange(n):
            z -= ((y << 4) + c) ^ (y + s) ^ ((y >> 5) + d)
            z &= op
            y -= ((z << 4) + a) ^ (z + s) ^ ((z >> 5) + b)
            y &= op
            s -= delta
            s &= op
        return struct.pack('>LL', y, z)

    def encrypt(self, v):
        END_CHAR = '\0'
        FILL_N_OR = 0xF8
        vl = len(v)
        filln = (8 - (vl + 2)) % 8 + 2
        fills = ''
        for i in xrange(filln):
            fills = fills + chr(220)
        v = (chr((filln - 2) | FILL_N_OR)
             + fills
             + v
             + END_CHAR * 7)
        tr = '\0' * 8
        to = '\0' * 8
        r = ''
        o = '\0' * 8
        for i in xrange(0, len(v), 8):
            o = self.xor(v[i:i + 8], tr)
            tr = self.xor(self.code(o, secret_key), to)
            to = o
            r += tr
        return r

    def decrypt(self, v):
        l = len(v)
        prePlain = self.decipher(v, secret_key)
        pos = (ord(prePlain[0]) & 0x07L) + 2
        r = prePlain
        preCrypt = v[0:8]
        for i in xrange(8, l, 8):
            x = self.xor(self.decipher(self.xor(v[i:i + 8], prePlain), secret_key), preCrypt)
            prePlain = self.xor(x, preCrypt)
            preCrypt = v[i:i + 8]
            r += x
        if r[-7:] != '\0' * 7:
            return None
        return r[pos + 1:-7]


if __name__ == '__main__':
    global secret_key
    secret_key = binascii.b2a_base64('ddfevzdfewrtgd34243fsfs')
    _3ds = _secret()

    print secret_key

    test()