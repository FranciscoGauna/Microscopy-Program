import objgraph
from time import sleep
from threading import Thread


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


def ends():
    a = A()
    sleep(1)
    print(a.b.counter)
    objgraph.show_refs([a], filename='sample-graph.png')
    return a.b


def never_ends():
    a = A()
    a.self_reference = a
    sleep(1)
    print(a.b.counter)
    objgraph.show_refs([a], filename='sample-graph.png')
    return a.b


b = ends()
print(b.running)
b.running = False