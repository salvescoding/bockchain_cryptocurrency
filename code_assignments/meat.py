from food import Food


class Meat(Food):

    def cook(self):
        print("The meat is cooking :)")



steak = Meat('Sirloin', 'Tasty')
steak.describe(steak)
steak.cook()
print(steak)
