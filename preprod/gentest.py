def a():
    for _a in range(10):
        yield _a


def c():
    for _c in range(11):
        yield _c


def b():
    a1 = a()
    for a2 in c():
        yield next(a1), a2


print(list(b()))