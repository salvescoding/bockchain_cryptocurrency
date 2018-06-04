names = ["Sergio", "Alves", "Nuno", "Nambia", "Marise", "Van", "Namagesco"]

for name in names:
    if len(name) >= 5 and "N" in name:
        print(name)

while len(names) > 0:
    names.pop()
    print(names)
