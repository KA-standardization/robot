# -*- coding:utf-8 -*-
import time
import heapq
import itertools
import collections

t_id = itertools.count(1)


class EventLoop(object):

    def __init__(self):
        self.ready = collections.deque()
        self.scheduled = []
        self.stop_ = False

    def call_soon(self, callbak, *args):
        self.ready.append((callbak, args))

    def call_later(self, delay, callbak, *args):
        t = time.time() + delay
        heapq.heappush(self.scheduled, (t, callbak, args))

    def run(self):
        while 1:
            self._run()
            if self.stop_:
                break

    def _run(self):
        t = time.time()
        if self.scheduled:
            if self.scheduled[0][0] < t:
                _, func, arg = heapq.heappop(self.scheduled)
                self.ready.append((func, arg))

        task_num = len(self.ready)
        for i in range(task_num):
            func, arg = self.ready.popleft()
            func(*arg)

    def stop(self):
        self.stop_ = True


class Future(object):

    def __init__(self):
        global loop
        self.res = None
        self.flag = False
        self.callbaks = []
        self._loop = loop

    def set_res(self, result):
        if self.flag:
            raise RuntimeError("res is not done")
        self.res = result
        self.flag = True
        for item in self.callbaks:
            # item()
            self._loop.call_soon(item)

    def get_res(self):
        if self.flag:
            return self.res
        else:
            raise RuntimeError("res is not done")

    def set_done_callbak(self, callbak):
        self.callbaks.append(callbak)

    def __await__(self):
        yield self
        return self.get_res()


class Task(Future):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self._id = "TID-{}".format(next(t_id))
        self._loop.call_soon(self.run)

    def run(self):
        print("T ID --> {}".format(self._id))
        if not self.flag:
            try:
                x = self.core.send(None)
            except StopIteration as e:
                self.set_res(e.value)
            else:
                assert isinstance(x, Future)
                x.set_done_callbak(self.run)
        print("task: {} res: ".format(self._id) + str(self.res))


async def foo(func, p):
    global loop
    f = Future()
    func(f, p)
    res = await f
    return res


async def task(func, p):
    res = await foo(func, p)
    return "task" + str(res)


loop = EventLoop()
