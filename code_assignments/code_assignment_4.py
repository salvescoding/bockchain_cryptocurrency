def normal(function):
    print(function(10))

normal(lambda el: el * 2)


def multiple_args(func, *args):
    for arg in args:
        print(func(arg))
        print("Result with format is {:^20.1f}".format(func(arg)))

multiple_args(lambda el: el * 2, 10, 20, 30, 40, 50)
