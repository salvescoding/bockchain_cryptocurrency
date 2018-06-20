class Food:

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return str(self.__dict__)

    # Static Method
    @staticmethod
    def describe(self):
        print("Name: {}, Kind of food: {}".format(self.name, self.kind))

    # Class method for describe
    # @classmethod
    # def describe(cls, name, kind):
    #     print("Name: {}, Kind of food: {}".format(name, kind))


# Class method
# Food.describe("Risotto", "Italian")


# Static method call
food = Food('Risotto', 'Italian')
food.describe(food)
print(food)
