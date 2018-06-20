from food import Food

class Fruit(Food):

  def clean(self):
      print("Fruit is fresh and clean")



fruit = Fruit('Apple', 'Acid')
fruit.clean()
fruit.describe(fruit)
print(fruit)
