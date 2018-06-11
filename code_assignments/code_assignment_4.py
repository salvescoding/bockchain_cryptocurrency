def normal(function):
    print(function(10))

normal(lambda el: el * 2)


def multiple_args(func, *args):
    for arg in args:
        print(func(arg))
        print("Result with format is {:^20.1f}".format(func(arg)))

multiple_args(lambda el: el * 2, 3, 4, 5, 6, 7)
