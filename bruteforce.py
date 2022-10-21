"""Brute force algorithm."""


import csv
from math import factorial

SHARES_FILE = "data/shares_list.csv"
MAX_INVESTMENT = 500

shares, all_combinations = [], []
best_combination = { 'shares': [], 'investment' : 0, 'profit': 0 }


class Share:
    """Shares class"""

    def __init__(self, name, price, profit) -> None:
        self.name = name
        self.price = price
        self.profit = price*(profit/100) # Convert percent profit in euros

    def __str__(self):
        return f"{self.name} / {self.price} € / {round(self.profit,2)} €"

"""Fill the "shares" list with share objects from the CSV file."""
def fill_shares_list():
    with open(SHARES_FILE) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for line in reader:
            shares.append(Share(line['name'], float(line['price']), float(line['profit'])))

"""Source code for 'itertools.combinations' function."""
def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def find_all_combinations():
    for i in range(1,len(shares)+1):
        for j in combinations(shares,i):
            all_combinations.append(j)
    

"""Calculate the total profit of a combination of shares."""
def calculate_combination_profit(combination):
        investment, profit = 0, 0
        for share in combination:
            investment += share.price
            if (investment > MAX_INVESTMENT):
                return None, None
            profit += share.profit
        return investment, profit

def keep_best_combination():
    for combination in all_combinations:
        combination_investment, combination_profit = calculate_combination_profit(combination)
        if combination_profit is not None:
            if combination_profit > best_combination['profit']:
                best_combination['shares'] = combination
                best_combination['investment'] = combination_investment
                best_combination['profit'] = combination_profit

def calculate_all_possible_theoretical_combinations(n):
    sum = 0
    for i in range(1,n+1):
        sum += factorial(n)/(factorial(i)*factorial(n-i))
    print(f"\nLe nombre de combinaisons théoriques possibles est de {int(sum)}.")

def display_result():
    calculate_all_possible_theoretical_combinations(len(shares))
    print(f"\nLe nombre de combinaisons trouvées est de {len(all_combinations)}.")
    print(f"\nLa meilleure combinaison d'actions est : \n")
    for share in best_combination['shares']:
        print(share)
    print(f"\npour un profit maximum de {round(best_combination['profit'],2)}")
    print(f"\net un investissement de {round(best_combination['investment'],2)}.\n")

def main():
    fill_shares_list()
    find_all_combinations()
    keep_best_combination()
    display_result()

if __name__ == "__main__":
    main()
