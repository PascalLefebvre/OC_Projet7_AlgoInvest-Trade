"""Brute force algorithm."""


import csv
from math import factorial
from itertools import combinations

ACTIONS_LIST_FILE = "ActionsList.csv"
MAX_INVESTMENT = 500

actions, all_actions, all_combinations = [], [], []
best_combination = { 'actions': [], 'investment' : 0, 'profit': 0 }


class Action:
    """Actions class"""

    def __init__(self, name, price, profit) -> None:
        self.name = name
        self.price = price
        self.profit = price*(profit/100) # Convert percent profit in euros        


"""Fill the "actions" list with action objects from the CSV file."""
def fill_actions_list():
    with open(ACTIONS_LIST_FILE) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for line in reader:
            actions.append(Action(line['name'], float(line['price']), float(line['profit'])))

def find_all_combinations():
    for i in range(1,len(actions)+1):
        for j in combinations(actions,i):
            all_combinations.append(j)
    

"""Calculate the total profit of a combination of actions."""
def calculate_combination_profit(combination):
        investment, profit = 0, 0
        for action in combination:
            investment += action.price
            if (investment > MAX_INVESTMENT):
                return None, None
            profit += action.profit
        return investment, profit

def keep_best_combination():
    for combination in all_combinations:
        combination_investment, combination_profit = calculate_combination_profit(combination)
        if combination_profit is not None:
            if combination_profit > best_combination['profit']:
                best_combination['actions'] = combination
                best_combination['investment'] = combination_investment
                best_combination['profit'] = combination_profit

def calculate_all_possible_theoretical_combinations(n):
    sum = 0
    for i in range(1,n+1):
        sum += factorial(n)/(factorial(i)*factorial(n-i))
    print(f"\nLe nombre de combinaisons théoriques possibles est de {sum}.")

def display_result():
    calculate_all_possible_theoretical_combinations(len(actions))
    print(f"\nLe nombre de combinaisons trouvées est de {len(all_combinations)}.")
    print(f"\nLa meilleure combinaison d'actions est : \n")
    for action in best_combination['actions']:
        print(action.name)
    print(f"\npour un profit maximum de {round(best_combination['profit'],2)}")
    print(f"\net un investissement de {round(best_combination['investment'],2)}.\n")

def main():
    fill_actions_list()
    find_all_combinations()
    keep_best_combination()
    display_result()

if __name__ == "__main__":
    main()
