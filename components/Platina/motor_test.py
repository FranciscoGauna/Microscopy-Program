from time import sleep
from threading import Thread


class C:
    def __init__(self):
        self.a = A()
        self.message = "Hello World"
        self.thread = Thread(target=self.method)

    def method(self):
        print(self.message)


class A:
    def __init__(self):
        self.b = B()
        self.thread = Thread(target=self.b.increment_counter)
        self.thread.start()

    def __del__(self):
        self.b.running = False


class B:
    def __init__(self):
        self.counter = 0
        self.running = True

    def increment_counter(self):
        while self.running:
            self.counter += 1
            sleep(0.1)


def fun():
    c = C()
    sleep(1)
    print(c.a.b.counter)


fun()
