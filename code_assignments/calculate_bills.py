flatmates_days = {
    'Marise': 0,
    'Sergio': 0,
    'Erika': 0
}
flatmates_total = {
    'Marise': 0,
    'Sergio': 0,
    'Erika': 0
}

total_days = 60


def calculate_amount_per_day(amount):
    return amount / 60


def calculate_individual_bill(total):
    bill = total / len(flatmates_days)
    for key in flatmates_total:
        if key in flatmates_days:
            flatmates_total[key] += bill


def calculate_bill_per_days(amount_of_days, amount_per_day):
    total = float(amount_of_days) * amount_per_day
    total = total / float(len(flatmates_days))
    calculate_individual_bill(total)


def flatmate_with_less_days():
    return min(flatmates_days, key=flatmates_days.get)


amount = float(input('Introduce your amount of the bill: '))
for key, value in flatmates_days.items():
    days = int(input(f'How many days {key} have been during this bill: '))
    flatmates_days[key] = days

amount_daily = (calculate_amount_per_day(amount))

while len(flatmates_days) > 0:
    less_days = flatmate_with_less_days()
    amount_of_days = flatmates_days[less_days]
    calculate_bill_per_days(amount_of_days, amount_daily)
    del flatmates_days[less_days]


for key, value in flatmates_total.items():
    print(f'{key}, have to pay: {value}')
